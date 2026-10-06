"""
Trace: learn data structures and algorithms by building intuition, then writing the code.
Every Run executes your code in a brand-new Docker container.

    python server.py              start it and open http://localhost:8000
    python server.py --port 9000  use another port
    docker compose up -d          run the server itself in Docker too (see docker-compose.yml)
    python server.py --check      verify every solution, starter and guided step in real containers

Needs Python 3.10+ and Docker Desktop. No pip installs.
"""
import argparse
import ast
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import uuid
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

FROZEN = getattr(sys, "frozen", False)        # running as the packaged desktop app (Trace.exe)
ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
COURSE = ROOT / "course"                # course/<stage>/<NN_topic>/{lesson.py, problems...}
SOLUTIONS = ROOT / "solutions"
WEB = ROOT / "web"
# Your code and progress. The desktop app keeps them in your user folder (its install folder may be read-only).
_DEFAULT_WORKSPACE = (Path(os.environ.get("LOCALAPPDATA") or Path.home()) / "Trace" / "workspace") if FROZEN else ROOT / "workspace"
WORKSPACE = Path(os.environ.get("TRACE_WORKSPACE") or _DEFAULT_WORKSPACE)
PROGRESS_FILE = WORKSPACE / "progress.json"

IMAGE = "trace-runner"
SANDBOX = [
    "--network", "none",                 # no internet from inside
    "--memory", "256m", "--memory-swap", "256m",
    "--cpus", "1",
    "--pids-limit", "64",
    "--read-only", "--tmpfs", "/tmp:rw,size=16m",
    "--cap-drop", "ALL",
    "--security-opt", "no-new-privileges",
]
SANDBOX_MODE = os.environ.get("TRACE_SANDBOX", "local")   # "local" (default: a fresh Python process) or "docker"
MEMORY_MB = 512                                          # memory cap for a local run
TEST_DEADLINE = 60      # seconds before a whole test run is killed
SCRIPT_DEADLINE = 20    # ... or a plain script run
MARK = "@@DSA_RESULT@@"

# Ladder order inside a topic. Solo problems sort by difficulty.
KINDS = ("snippet", "guided", "easy", "medium", "hard", "build")
RANK = {k: i for i, k in enumerate(KINDS)}


# ── Docker ───────────────────────────────────────────────────────────────────

class Docker:
    """Tracks whether Docker is usable, and builds the sandbox image once."""

    def __init__(self):
        self.state = "checking"          # checking | missing | stopped | building | ready | broken
        self.detail = ""
        self.lock = threading.Lock()

    def refresh(self):
        if self.state in ("ready", "building"):
            return
        with self.lock:
            if self.state == "ready":
                return
            try:
                info = subprocess.run(["docker", "info", "--format", "{{.ServerVersion}}"],
                                      capture_output=True, text=True, timeout=20)
            except FileNotFoundError:
                self.state, self.detail = "missing", ""
                return
            except subprocess.TimeoutExpired:
                self.state, self.detail = "stopped", ""
                return
            if info.returncode != 0 or not info.stdout.strip():
                self.state, self.detail = "stopped", ""
                return
            self.state = "building"
        build = subprocess.run(
            ["docker", "build", "-q", "-t", IMAGE, "-f", str(ROOT / "runner" / "Dockerfile"), str(ROOT)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        if build.returncode == 0:
            self.state, self.detail = "ready", ""
            POOL.refill_in_background()     # pre-start sandboxes so the first Run doesn't wait
        else:
            self.state, self.detail = "broken", (build.stderr or build.stdout)[-3000:]

    def refresh_in_background(self):
        threading.Thread(target=self.refresh, daemon=True).start()

    def status(self):
        return {"state": self.state, "detail": self.detail}


DOCKER = Docker()


def sandbox_status():
    if SANDBOX_MODE == "local":
        return {"state": "ready", "detail": "", "mode": "local"}
    return {**DOCKER.status(), "mode": "docker"}


def refresh_sandbox():
    if SANDBOX_MODE == "docker":
        DOCKER.refresh_in_background()
    elif not POOL.idle:
        POOL.refill_in_background()


# ── Local sandbox: one fresh Python process per run ─────────────────────────

BUNDLED_PYTHON = ROOT / "runtime" / "python" / ("python.exe" if os.name == "nt" else "bin/python3")


def _judge_command():
    # The bundled runtime (official embeddable Python 3.14) when present, so everyone runs the same Python.
    python = str(BUNDLED_PYTHON) if BUNDLED_PYTHON.exists() else sys.executable
    return [python, "-X", "utf8", str(ROOT / "runner" / "judge.py")]


def _limit_unix():                                  # runs in the child before exec (Linux/macOS)
    import resource
    limit = MEMORY_MB * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (limit, limit))


def _windows_job(proc):
    """Put the process in a Windows Job Object: a memory cap, no child processes, and it dies with the job."""
    try:
        import ctypes
        from ctypes import wintypes
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)

        class Basic(ctypes.Structure):
            _fields_ = [("PerProcessUserTimeLimit", ctypes.c_longlong), ("PerJobUserTimeLimit", ctypes.c_longlong),
                        ("LimitFlags", wintypes.DWORD), ("MinimumWorkingSetSize", ctypes.c_size_t),
                        ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", wintypes.DWORD),
                        ("Affinity", ctypes.c_size_t), ("PriorityClass", wintypes.DWORD), ("SchedulingClass", wintypes.DWORD)]

        class IoCounters(ctypes.Structure):
            _fields_ = [(n, ctypes.c_ulonglong) for n in ("ReadOps", "WriteOps", "OtherOps", "ReadBytes", "WriteBytes", "OtherBytes")]

        class Extended(ctypes.Structure):
            _fields_ = [("BasicLimitInformation", Basic), ("IoInfo", IoCounters), ("ProcessMemoryLimit", ctypes.c_size_t),
                        ("JobMemoryLimit", ctypes.c_size_t), ("PeakProcessMemoryUsed", ctypes.c_size_t),
                        ("PeakJobMemoryUsed", ctypes.c_size_t)]

        k32.CreateJobObjectW.restype = wintypes.HANDLE
        k32.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
        k32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        k32.CloseHandle.argtypes = [wintypes.HANDLE]
        job = k32.CreateJobObjectW(None, None)
        info = Extended()
        info.BasicLimitInformation.LimitFlags = 0x100 | 0x8 | 0x2000     # PROCESS_MEMORY | ACTIVE_PROCESS | KILL_ON_JOB_CLOSE
        info.BasicLimitInformation.ActiveProcessLimit = 1                # user code can't start other programs
        info.ProcessMemoryLimit = MEMORY_MB * 1024 * 1024
        k32.SetInformationJobObject(job, 9, ctypes.byref(info), ctypes.sizeof(info))   # 9 = extended limits
        k32.AssignProcessToJobObject(job, int(proc._handle))
        proc._job = (k32, job)
    except Exception:  # noqa: BLE001 - limits are best-effort; the time limit still applies
        proc._job = None


def _release(proc):
    job = getattr(proc, "_job", None)
    if job:
        k32, handle = job
        k32.CloseHandle(handle)                 # KILL_ON_JOB_CLOSE: nothing can outlive the run
        proc._job = None


def _spawn_local():
    env = {**os.environ, "PYTHONPATH": str(ROOT), "PYTHONIOENCODING": "utf-8",
           "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUNBUFFERED": "1"}
    extra = {"creationflags": 0x08000000} if os.name == "nt" else {"preexec_fn": _limit_unix}   # CREATE_NO_WINDOW
    proc = subprocess.Popen(_judge_command(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, encoding="utf-8", errors="replace", cwd=tempfile.gettempdir(), env=env, **extra)
    if os.name == "nt":
        _windows_job(proc)
    return proc


def docker_problem():
    """None if the sandbox is usable, otherwise a message the page can show."""
    if SANDBOX_MODE == "local":
        return None
    DOCKER.refresh()
    if DOCKER.state == "ready":
        return None
    return {
        "missing": "Docker isn't installed. Install Docker Desktop, then restart this server.",
        "stopped": "Docker Desktop isn't running. Start it, wait until it says it's running, then press Run again.",
        "building": "The Python sandbox image is still being prepared. Try again in a few seconds.",
        "broken": "The sandbox image failed to build:\n" + DOCKER.detail,
    }.get(DOCKER.state, "Docker isn't ready yet.")


class WarmPool:
    """A few sandbox containers started ahead of time. Each one has already booted Python and
    loaded the judge, and is blocked reading its job from stdin. A Run takes one (single use,
    still thrown away afterwards), so nobody waits for container start-up."""

    SIZE = 2
    MAX_AGE = 600           # seconds; old idle containers are replaced, not reused

    def __init__(self):
        self.idle = []
        self.lock = threading.Lock()

    def _spawn(self):
        if SANDBOX_MODE == "local":
            return None, _spawn_local(), time.monotonic()
        name = f"trace-run-{uuid.uuid4().hex[:8]}"
        proc = subprocess.Popen(["docker", "run", "--rm", "-i", "--name", name, *SANDBOX, IMAGE],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, encoding="utf-8", errors="replace")
        return name, proc, time.monotonic()

    def _refill(self):
        with self.lock:
            missing = self.SIZE - len(self.idle)
        for _ in range(max(0, missing)):
            try:
                warm = self._spawn()
            except OSError:
                return
            with self.lock:
                self.idle.append(warm)

    def refill_in_background(self):
        if SANDBOX_MODE == "local" or DOCKER.state == "ready":
            threading.Thread(target=self._refill, daemon=True).start()

    def take(self):
        with self.lock:
            while self.idle:
                name, proc, born = self.idle.pop(0)
                if proc.poll() is None and time.monotonic() - born < self.MAX_AGE:
                    break
                self._discard(name, proc)
            else:
                name = proc = None
        self.refill_in_background()
        return (name, proc) if proc else self._spawn()[:2]

    @staticmethod
    def _discard(name, proc):
        def go():
            proc.kill()
            _release(proc)
            if name:
                subprocess.run(["docker", "rm", "-f", name], capture_output=True)
        threading.Thread(target=go, daemon=True).start()


POOL = WarmPool()


def run_in_container(job, deadline):
    """Hand the job to a fresh, locked-down container (pre-started if one is ready) and throw it away."""
    name, proc = POOL.take()
    start = time.perf_counter()
    try:
        stdout, stderr = proc.communicate(json.dumps(job), timeout=deadline)
    except subprocess.TimeoutExpired:
        proc.kill()
        _release(proc)
        if name:
            subprocess.run(["docker", "rm", "-f", name], capture_output=True)
        return {"seconds": deadline, "exit_code": None, "stdout": "", "stderr": "",
                "killed": f"The run was stopped after {deadline} seconds."}
    _release(proc)
    result = {"seconds": round(time.perf_counter() - start, 2), "exit_code": proc.returncode,
              "stdout": stdout, "stderr": stderr, "killed": None}
    if proc.returncode == 137:
        result["killed"] = "The container ran out of memory (256 MB limit) and was stopped."
    elif proc.returncode == 125:
        result["killed"] = "Docker couldn't start the container:\n" + proc.stderr.strip()
    return result


def run_tests(problem, code, custom="", upto=None):
    job = {"mode": "test", "name": problem["name"], "problem": problem["source"], "code": code,
           "custom": custom, "upto": upto}
    run = run_in_container(job, TEST_DEADLINE)
    reply = {"seconds": run["seconds"]}
    if MARK in run["stdout"]:
        reply["report"] = json.loads(run["stdout"].rsplit(MARK, 1)[1])
    else:
        reply["crash"] = run["killed"] or (run["stderr"] or run["stdout"] or "The container exited unexpectedly.").strip()
    return reply


def run_script(code):
    run = run_in_container({"mode": "run", "code": code}, SCRIPT_DEADLINE)
    return {"seconds": run["seconds"], "exit_code": run["exit_code"],
            "output": run["stdout"] + run["stderr"], "killed": run["killed"]}


# ── Course ───────────────────────────────────────────────────────────────────

def folder_label(name):
    """'06_two_pointers' -> 'Two pointers'"""
    text = re.sub(r"^\d+_", "", name).replace("_", " ")
    return text[:1].upper() + text[1:]


def parse_lesson(path):
    """A lesson file is a docstring of notes (light markdown) followed by runnable example code."""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    first = tree.body[0] if tree.body else None
    notes, code = "", source
    if isinstance(first, ast.Expr) and isinstance(getattr(first, "value", None), ast.Constant) \
            and isinstance(first.value.value, str):
        notes = first.value.value.strip("\n")
        code = "\n".join(source.splitlines()[first.end_lineno:]).lstrip("\n")
    title = next((line[2:].strip() for line in notes.splitlines() if line.startswith("# ")), "")
    return {"notes": notes, "code": code, "title": title}


def split_statement(text):
    """Pull 'Aim for:' and 'Hint:' blocks out of a problem statement."""
    out, extra, current = [], {"aim": [], "hint": []}, None
    for line in text.splitlines():
        m = re.match(r"^(Aim for|Hint):\s*(.*)$", line)
        if m:
            current = "aim" if m.group(1) == "Aim for" else "hint"
            extra[current].append(m.group(2).strip())
        elif current and line.startswith(" ") and line.strip():
            extra[current].append(line.strip())
        else:
            current = None
            out.append(line)
    return "\n".join(out).strip("\n"), " ".join(extra["aim"]), " ".join(extra["hint"])


_MODULES = {}


def load_module(path):
    """Execute a problem file (our own course content) to read STEPS / TESTS. Cached by mtime."""
    key = (str(path), path.stat().st_mtime)
    if key not in _MODULES:
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
        namespace = {"__name__": "problem"}
        exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), namespace)
        _MODULES[key] = namespace
    return _MODULES[key]


def _prelude_names():
    """Names the sandbox preloads into every run (runner/prelude.py)."""
    for p in (str(ROOT), str(ROOT / "runner")):
        if p not in sys.path:
            sys.path.insert(0, p)
    try:
        from prelude import PRELUDE
        return PRELUDE
    except Exception:  # noqa: BLE001 - without it, starters just keep their import lines
        return {}


PRELUDE = _prelude_names()


def prelude_covers(node):
    """True if every name an import statement binds is already preloaded, as the same object."""
    if isinstance(node, ast.ImportFrom):
        if not node.module or node.level:
            return False
        bound = [(a.asname or a.name, a.name) for a in node.names]
        try:
            module = __import__(node.module, fromlist=["_"])
        except ImportError:
            return False
        return all(alias in PRELUDE and PRELUDE[alias] is getattr(module, name, None) for alias, name in bound)
    return all((a.asname or a.name) in PRELUDE and "." not in a.name for a in node.names)


def parse_problem(path):
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    doc = (ast.get_docstring(tree, clean=False) or "").strip("\n")
    lines = doc.splitlines() or [path.stem]
    header = lines[0]
    tag = re.search(r"\[(snippet|guided|easy|medium|hard|build)\]", header)
    kind = tag.group(1) if tag else "medium"
    statement, aim, hint = split_statement("\n".join(lines[1:]))

    # Starter code = the file's imports + every public function/class, exactly as written.
    src_lines = source.splitlines()
    parts, imports, constants, seen_def = [], [], [], False
    for node in tree.body:
        segment = "\n".join(src_lines[node.lineno - 1: node.end_lineno])
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if not prelude_covers(node):        # preloaded names need no import line in the starter
                imports.append(re.sub(r"\s+# noqa.*$", "", segment))
        elif isinstance(node, ast.Assign) and not seen_def:
            constants.append(segment)          # e.g. MOD = 1_000_000_007, declared above the function
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            seen_def = True
            if not node.name.startswith("_") and not node.name.isupper():
                start = node.decorator_list[0].lineno if node.decorator_list else node.lineno
                parts.append("\n".join(src_lines[start - 1: node.end_lineno]))
    head = "\n".join(imports) + ("\n\n" if imports and constants else "") + "\n".join(constants)
    starter = (head + "\n\n\n" if head else "") + "\n\n\n".join(parts) + "\n"

    module = load_module(path)
    steps = [{"title": st.get("title", f"Step {i + 1}"), "text": st.get("text", ""), "hint": st.get("hint", ""),
              "tests": len(st["tests"])} for i, st in enumerate(module.get("STEPS") or [])]
    tests = sum(s["tests"] for s in steps) if steps else len(module.get("TESTS") or [])

    return {
        "name": path.stem,
        "title": header.split("[")[0].strip() or path.stem,
        "kind": "solo" if kind in ("easy", "medium", "hard") else kind,
        "difficulty": kind if kind in ("easy", "medium", "hard") else "",
        "rank": RANK[kind],
        "statement": statement,
        "aim": aim,
        "hint": hint,
        "starter": starter,
        "source": source,
        "tests": tests,
        "steps": steps,
        "is_class": bool(module.get("CLASS")),
        "has_solution": (SOLUTIONS / f"{path.stem}.py").exists(),
    }


class CourseCache:
    """The parsed course, kept in memory. Reading ~200 files per request is slow (especially
    through a Docker bind mount on Windows), so a background watcher re-scans file timestamps
    every couple of seconds and re-parses only what changed. Edits still show up on refresh."""

    def __init__(self):
        self.lock = threading.Lock()
        self.signature = None
        self.course = None
        self.parsed = {}        # path -> (key, parsed problem or lesson)

    @staticmethod
    def scan():
        sig = {}
        for base in (COURSE, SOLUTIONS):
            for path in base.rglob("*.py"):
                try:
                    sig[str(path)] = path.stat().st_mtime_ns
                except OSError:
                    pass
        return sig

    def _cached(self, path, key, parse):
        hit = self.parsed.get(str(path))
        if hit and hit[0] == key:
            return hit[1]
        value = parse(path)
        self.parsed[str(path)] = (key, value)
        return value

    def _build(self, sig):
        topics, problems = [], {}
        for stage_dir in sorted(d for d in COURSE.iterdir() if d.is_dir()):
            for topic_dir in sorted(d for d in stage_dir.iterdir() if d.is_dir()):
                number = int(re.match(r"^(\d+)", topic_dir.name).group(1))
                lesson_path = topic_dir / "lesson.py"
                lesson = (self._cached(lesson_path, sig.get(str(lesson_path)), parse_lesson)
                          if str(lesson_path) in sig else None)
                found = []
                for p in sorted(topic_dir.glob("*.py")):
                    if p.name == "lesson.py" or p.name.startswith("_"):
                        continue
                    sol = SOLUTIONS / f"{p.stem}.py"
                    found.append(dict(self._cached(p, (sig.get(str(p)), sig.get(str(sol))), parse_problem)))
                found.sort(key=lambda p: (p["rank"], p["title"].lower()))
                topic = {
                    "id": topic_dir.name, "n": number,
                    "title": (lesson and lesson["title"]) or folder_label(topic_dir.name),
                    "stage": folder_label(stage_dir.name),
                    "lesson": lesson,
                    "items": [p["name"] for p in found],
                }
                for p in found:
                    p.update(topic_id=topic["id"], topic_n=number, topic=topic["title"])
                    problems[p["name"]] = p
                topics.append(topic)
        return topics, problems

    def get(self):
        with self.lock:
            if self.course is None:
                self.signature = self.scan()
                self.course = self._build(self.signature)
            return self.course

    def poll(self):
        sig = self.scan()
        with self.lock:
            if sig != self.signature:
                self.course = self._build(sig)
                self.signature = sig

    def watch(self, every=2.0):
        def loop():
            while True:
                time.sleep(every)
                try:
                    self.poll()
                except Exception as exc:  # noqa: BLE001 - a half-saved file shouldn't kill the watcher
                    sys.stderr.write(f"  course reload failed: {exc}\n")
        threading.Thread(target=loop, daemon=True).start()


COURSE_CACHE = CourseCache()


def load_course():
    """Topics in study order, each with its ladder: snippet, guided, solo (easy → hard), build."""
    return COURSE_CACHE.get()


_PLANS = {"key": None, "value": {"plans": [], "reported": {}, "reported_note": ""}}


def load_plans():
    """Study plans (course/plans.json): named, ordered lists of problems. Cached by mtime."""
    path = COURSE / "plans.json"
    try:
        key = path.stat().st_mtime_ns
    except OSError:
        return _PLANS["value"]
    if key != _PLANS["key"]:
        data = json.loads(path.read_text(encoding="utf-8"))
        problems = load_course()[1]
        for plan in data.get("plans", []):
            for section in plan["sections"]:
                section["items"] = [n for n in section["items"] if n in problems]   # ignore typos, never crash
        _PLANS.update(key=key, value=data)
    return _PLANS["value"]


def public_problem(p):
    keys = ("name", "title", "kind", "difficulty", "statement", "aim", "hint", "tests", "steps", "is_class",
            "has_solution", "topic_id", "topic_n", "topic")
    return {k: p[k] for k in keys}


class StaticCache:
    """Web files kept in memory, keyed by modification time, with ETags so reloads are 304s."""

    def __init__(self):
        self.files = {}
        self.zipped = {}
        self.lock = threading.Lock()

    def get(self, path):
        stat = path.stat()
        key = (stat.st_mtime_ns, stat.st_size)
        with self.lock:
            hit = self.files.get(path)
            if hit and hit[0] == key:
                return hit[1], hit[2]
        data = path.read_bytes()
        etag = f'"{key[0]:x}-{key[1]:x}"'
        with self.lock:
            self.files[path] = (key, data, etag)
            self.zipped.pop(path, None)
        return data, etag

    def gzipped(self, path, data):
        import gzip
        with self.lock:
            hit = self.zipped.get(path)
            if hit and hit[0] is data:
                return hit[1]
        body = gzip.compress(data, 6)
        with self.lock:
            self.zipped[path] = (data, body)
        return body


STATIC = StaticCache()


# ── Progress and saved code ──────────────────────────────────────────────────

PROGRESS_LOCK = threading.Lock()


def load_progress():
    try:
        progress = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        progress = {}
    progress.setdefault("problems", {})
    progress.setdefault("unlocked", [])
    return progress


def update_progress(change):
    with PROGRESS_LOCK:
        progress = load_progress()
        change(progress)
        WORKSPACE.mkdir(exist_ok=True)
        PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")
        return progress


def record_result(problem, tests):
    passed = sum(t["status"] == "pass" for t in tests)
    steps_done = 0
    for i in range(len(problem["steps"])):
        mine = [t for t in tests if t.get("step") == i]
        if mine and all(t["status"] == "pass" for t in mine):
            steps_done = i + 1
        else:
            break
    full = len(tests) == problem["tests"] and passed == len(tests)

    def change(progress):
        old = progress["problems"].get(problem["name"], {})
        progress["problems"][problem["name"]] = {
            "passed": passed, "total": problem["tests"],
            "solved": old.get("solved", False) or full,
            "steps": max(old.get("steps", 0), steps_done),
        }
    return update_progress(change)


def saved_code_path(name):
    return WORKSPACE / "code" / f"{name}.py"


# ── HTTP ─────────────────────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):
    server_version = "Trace/2.0"

    def log_message(self, fmt, *args):
        if len(args) > 1 and str(args[1]).startswith(("4", "5")):
            sys.stderr.write(f"  {self.command} {self.path} {args[1]}\n")

    def send_json(self, data, status=HTTPStatus.OK):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def fail(self, message, status=HTTPStatus.BAD_REQUEST):
        self.send_json({"error": message}, status)

    def body(self):
        length = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(length) or b"{}")

    def serve_static(self, rel):
        path = (WEB / (rel or "index.html")).resolve()
        if WEB.resolve() not in path.parents or not path.is_file():
            return self.fail("Not found", HTTPStatus.NOT_FOUND)
        data, etag = STATIC.get(path)
        if self.headers.get("If-None-Match") == etag:      # browser already has this version
            self.send_response(HTTPStatus.NOT_MODIFIED)
            self.send_header("ETag", etag)
            self.end_headers()
            return
        types = {".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".ico": "image/x-icon"}
        text = path.suffix in (".html", ".css", ".js", ".svg")
        gz = text and "gzip" in (self.headers.get("Accept-Encoding") or "") and len(data) > 1400
        body = STATIC.gzipped(path, data) if gz else data
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", types.get(path.suffix, "application/octet-stream") + ("; charset=utf-8" if text else ""))
        self.send_header("Content-Length", str(len(body)))
        if gz:
            self.send_header("Content-Encoding", "gzip")
        self.send_header("Cache-Control", "no-cache")      # always revalidate, so edits show on refresh
        self.send_header("ETag", etag)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        query = {k: v[0] for k, v in parse_qs(url.query).items()}
        route = url.path

        if route == "/api/course":
            refresh_sandbox()
            topics, problems = load_course()
            return self.send_json({
                "docker": sandbox_status(),
                "topics": [{**{k: v for k, v in t.items() if k != "lesson"}, "has_lesson": bool(t["lesson"])}
                           for t in topics],
                "problems": {n: {k: p[k] for k in ("name", "title", "kind", "difficulty", "tests", "topic_id")}
                             | {"steps": len(p["steps"])} for n, p in problems.items()},
                "progress": load_progress(),
                "plans": load_plans(),
            })

        if route == "/api/docker":
            refresh_sandbox()
            return self.send_json(sandbox_status())

        if route == "/api/problem":
            problem = load_course()[1].get(query.get("name", ""))
            if not problem:
                return self.fail("Unknown problem", HTTPStatus.NOT_FOUND)
            saved = saved_code_path(problem["name"])
            data = public_problem(problem)
            data["starter"] = problem["starter"]
            plans = load_plans()
            data["reported"] = plans.get("reported", {}).get(problem["name"], [])
            data["reported_note"] = plans.get("reported_note", "")
            data["in_plans"] = [pl["title"] for pl in plans.get("plans", [])
                                if any(problem["name"] in s["items"] for s in pl["sections"])]
            data["code"] = saved.read_text(encoding="utf-8") if saved.exists() else problem["starter"]
            return self.send_json(data)

        if route == "/api/lesson":
            topic = next((t for t in load_course()[0] if t["id"] == query.get("topic")), None)
            if not topic or not topic["lesson"]:
                return self.fail("Unknown lesson", HTTPStatus.NOT_FOUND)
            return self.send_json(topic["lesson"])

        if route == "/api/solution":
            problem = load_course()[1].get(query.get("name", ""))
            if not problem or not problem["has_solution"]:
                return self.fail("No reference solution", HTTPStatus.NOT_FOUND)
            return self.send_json({"code": (SOLUTIONS / f"{problem['name']}.py").read_text(encoding="utf-8")})

        if route.startswith("/api/"):
            return self.fail("Not found", HTTPStatus.NOT_FOUND)
        return self.serve_static(route.lstrip("/"))

    def do_POST(self):
        route = urlparse(self.path).path
        try:
            data = self.body()
        except ValueError:
            return self.fail("Request body must be JSON")
        code = data.get("code", "")
        if not isinstance(code, str) or len(code) > 200_000:
            return self.fail("Code must be text under 200 KB")
        problem = load_course()[1].get(data.get("name", ""))

        if route == "/api/save":
            if not problem:
                return self.fail("Unknown problem")
            path = saved_code_path(problem["name"])
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(code, encoding="utf-8")
            return self.send_json({"saved": True})

        if route == "/api/reset":
            if not problem:
                return self.fail("Unknown problem")
            saved_code_path(problem["name"]).unlink(missing_ok=True)
            return self.send_json({"code": problem["starter"]})

        if route == "/api/unlock":
            if not problem:
                return self.fail("Unknown problem")

            def unlock(progress):
                if problem["name"] not in progress["unlocked"]:
                    progress["unlocked"].append(problem["name"])
            return self.send_json({"progress": update_progress(unlock)})

        if route == "/api/reset-progress":
            def wipe(progress):
                progress["problems"], progress["unlocked"] = {}, []
            return self.send_json({"progress": update_progress(wipe)})

        if route == "/api/test":
            if not problem:
                return self.fail("Unknown problem")
            blocked = docker_problem()
            if blocked:
                return self.send_json({"docker_error": blocked, "docker": sandbox_status()})
            record = data.get("save", True) is not False     # "save": false = a dry run: no code or progress written
            if record:
                path = saved_code_path(problem["name"])
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(code, encoding="utf-8")
            upto = data.get("upto")
            reply = run_tests(problem, code, str(data.get("custom") or "")[:2000], int(upto) if upto else None)
            tests = reply.get("report", {}).get("tests", [])
            if record and tests and not all(t["status"] == "todo" for t in tests):
                record_result(problem, tests)
            reply["progress"] = load_progress()
            return self.send_json(reply)

        if route == "/api/run":
            blocked = docker_problem()
            if blocked:
                return self.send_json({"docker_error": blocked, "docker": sandbox_status()})
            return self.send_json(run_script(code))

        self.fail("Not found", HTTPStatus.NOT_FOUND)


# ── Self-check ───────────────────────────────────────────────────────────────

def check(only=None):
    """Every reference solution must pass every test (every guided step), and every
    untouched starter must report 'todo'. All inside the real sandbox."""
    if SANDBOX_MODE == "docker":
        print("Preparing the container image...")
        DOCKER.refresh()
        if DOCKER.state != "ready":
            print(docker_problem())
            return 1
    else:
        print("Using the local sandbox (a fresh Python process per run)...")
    topics, problems = load_course()
    failures = 0
    for topic in topics:
        for name in topic["items"]:
            if only and not any(o in name or o in topic["id"] for o in only):
                continue
            problem = problems[name]
            sol_path = SOLUTIONS / f"{name}.py"
            if not sol_path.exists():
                print(f"  FAIL {name:<34} no reference solution")
                failures += 1
                continue
            reply = run_tests(problem, sol_path.read_text(encoding="utf-8"))
            tests = reply.get("report", {}).get("tests", [])
            ok = bool(tests) and len(tests) == problem["tests"] and all(t["status"] == "pass" for t in tests)
            stub = run_tests(problem, problem["starter"])
            stub_tests = stub.get("report", {}).get("tests", [])
            stub_ok = bool(stub_tests) and all(t["status"] == "todo" for t in stub_tests)
            failures += not (ok and stub_ok)
            label = f"{topic['n']:02} {problem['kind'][:7]:<7} {name}"
            slowest = max((t.get("ms", 0) for t in tests), default=0)
            print(f"  {'ok  ' if ok and stub_ok else 'FAIL'} {label:<50} {len(tests):>2} tests  slowest {slowest:7.1f} ms")
            if not ok:
                bad = [t for t in tests if t["status"] != "pass"][:3]
                print("        ", json.dumps(bad or reply)[:1500])
            if not stub_ok:
                print("         starter didn't report 'todo':", json.dumps(stub)[:600])
    print("\nAll good." if not failures else f"\n{failures} problem(s).")
    return 1 if failures else 0


def start_server(host="127.0.0.1", port=8000):
    """Prepare the course and sandbox, and return a ready (not yet serving) HTTP server."""
    refresh_sandbox()
    load_course()                   # parse the course once up front...
    COURSE_CACHE.watch()            # ...then only re-parse files that change
    return ThreadingHTTPServer((host, port), Handler)   # local only by default: it runs code


def main():
    global SANDBOX_MODE
    parser = argparse.ArgumentParser(description="Trace")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--host", default="127.0.0.1", help="address to listen on (0.0.0.0 inside Docker)")
    parser.add_argument("--no-browser", action="store_true", help="don't open a browser tab")
    parser.add_argument("--check", nargs="*", metavar="FILTER", help="verify solutions and starters in the sandbox")
    parser.add_argument("--sandbox", choices=("local", "docker"), default=None,
                        help="where code runs: a local Python process (default) or a Docker container")
    args = parser.parse_args()
    if args.sandbox:
        SANDBOX_MODE = args.sandbox

    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    if args.check is not None:
        return check(args.check)

    server = start_server(args.host, args.port)
    url = f"http://localhost:{args.port}"
    where = "a fresh Docker container" if SANDBOX_MODE == "docker" else "a fresh, isolated Python process"
    print(f"\n  Trace running at {url}")
    print(f"  Each Run uses {where}. Press Ctrl+C to stop.\n")
    if not args.no_browser:
        threading.Timer(0.6, webbrowser.open, [url]).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Stopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
