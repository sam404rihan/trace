"""
DSA Playground — a hands-on data structures & algorithms course, basics to advanced.
Every time you press Run, your code executes in a brand-new Docker container.

    python server.py              start it and open http://localhost:8000
    python server.py --port 9000  use another port
    python server.py --check      verify every solution, stub and lesson in containers

Needs Python 3.10+ and Docker Desktop. No pip installs.
"""
import argparse
import ast
import json
import re
import subprocess
import sys
import threading
import time
import uuid
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
COURSE = ROOT / "course"                # course/<stage>/<topic>/{lesson.py, problem.py...}
SOLUTIONS = ROOT / "solutions"
WEB = ROOT / "web"
WORKSPACE = ROOT / "workspace"          # your code and progress live here
PROGRESS_FILE = WORKSPACE / "progress.json"
SCRATCH_FILE = WORKSPACE / "scratch.py"
EXAMPLE_DIRS = ("structures", "algorithms")

IMAGE = "dsa-playground-runner"
SANDBOX = [
    "--network", "none",                 # no internet from inside
    "--memory", "256m", "--memory-swap", "256m",
    "--cpus", "1",
    "--pids-limit", "64",
    "--read-only", "--tmpfs", "/tmp:rw,size=16m",
    "--cap-drop", "ALL",
    "--security-opt", "no-new-privileges",
]
TEST_DEADLINE = 40      # seconds before we kill a test container outright
SCRIPT_DEADLINE = 20    # ... or a scratchpad / example run
MARK = "@@DSA_RESULT@@"

SCRATCH_STARTER = '''\
# Scratchpad: write any Python here and press Run.
# It runs in a fresh container. The playground's own code is importable:
#   helpers     ListNode, TreeNode, build_list, build_tree, print_tree
#   structures  linked_list, stack_queue, hash_map, bst, heap, graph, trie, union_find
#   algorithms  sorting

from structures.bst import BST

tree = BST([8, 3, 10, 1, 6, 14, 4, 7, 13])
print(tree)
print("in-order:", tree.inorder())
'''


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
        self._build()

    def _build(self):
        build = subprocess.run(
            ["docker", "build", "-q", "-t", IMAGE, "-f", str(ROOT / "runner" / "Dockerfile"), str(ROOT)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        if build.returncode == 0:
            self.state, self.detail = "ready", ""
        else:
            self.state, self.detail = "broken", (build.stderr or build.stdout)[-3000:]

    def refresh_in_background(self):
        threading.Thread(target=self.refresh, daemon=True).start()

    def status(self):
        return {"state": self.state, "detail": self.detail}


DOCKER = Docker()


def run_in_container(job, deadline):
    """Start a fresh, locked-down container, feed it the job, and throw it away."""
    name = f"dsa-run-{uuid.uuid4().hex[:8]}"
    cmd = ["docker", "run", "--rm", "-i", "--name", name, *SANDBOX, IMAGE]
    start = time.perf_counter()
    try:
        proc = subprocess.run(cmd, input=json.dumps(job), capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=deadline)
    except subprocess.TimeoutExpired:
        subprocess.run(["docker", "rm", "-f", name], capture_output=True)
        return {"container": name, "seconds": deadline, "exit_code": None, "stdout": "", "stderr": "",
                "killed": f"The container was stopped after {deadline} seconds."}
    result = {
        "container": name,
        "seconds": round(time.perf_counter() - start, 2),
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "killed": None,
    }
    if proc.returncode == 137:
        result["killed"] = "The container ran out of memory (256 MB limit) and was stopped."
    elif proc.returncode == 125:
        result["killed"] = "Docker couldn't start the container:\n" + proc.stderr.strip()
    return result


# ── Problems, examples and saved work ───────────────────────────────────────

def folder_label(name):
    """'06_two_pointers' -> 'Two pointers'"""
    text = re.sub(r"^\d+_", "", name).replace("_", " ")
    return text[:1].upper() + text[1:]


def parse_lesson(path):
    """A lesson file is a docstring of notes (light markdown) followed by runnable code."""
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


def parse_problem(path):
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    doc = (ast.get_docstring(tree, clean=False) or "").strip("\n")
    lines = doc.splitlines() or [path.stem]
    header = lines[0]
    level = re.search(r"\[(easy|medium|hard)\]", header)

    # Starter code = the file's imports + the function stub, exactly as written.
    src_lines = source.splitlines()
    imports, function = [], ""
    tests = 0
    for node in tree.body:
        segment = "\n".join(src_lines[node.lineno - 1: node.end_lineno])
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(re.sub(r"\s+# noqa.*$", "", segment))
        elif isinstance(node, ast.FunctionDef) and node.name == path.stem:
            function = segment
        elif isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "TESTS" for t in node.targets):
            tests = len(getattr(node.value, "elts", []))
    starter = ("\n".join(imports) + "\n\n\n" if imports else "") + function + "\n"

    return {
        "name": path.stem,
        "title": header.split("[")[0].strip() or path.stem,
        "difficulty": level.group(1) if level else "",
        "statement": "\n".join(lines[1:]).strip("\n"),
        "starter": starter,
        "source": source,
        "tests": tests,
        "has_solution": (SOLUTIONS / f"{path.stem}.py").exists(),
    }


def load_course():
    """Stages -> topics -> problems, in study order. Easier problems come first within a topic."""
    rank = {"easy": 0, "medium": 1, "hard": 2, "": 3}
    stages, topics, problems = [], {}, {}
    for stage_dir in sorted(d for d in COURSE.iterdir() if d.is_dir()):
        stage = {"id": stage_dir.name, "title": folder_label(stage_dir.name), "topics": []}
        stages.append(stage)
        for topic_dir in sorted(d for d in stage_dir.iterdir() if d.is_dir()):
            lesson_path = topic_dir / "lesson.py"
            lesson = parse_lesson(lesson_path) if lesson_path.exists() else None
            number = re.match(r"^(\d+)", topic_dir.name)
            topic = {
                "id": topic_dir.name,
                "number": int(number.group(1)) if number else 0,
                "title": (lesson and lesson["title"]) or folder_label(topic_dir.name),
                "stage": stage["title"],
                "has_lesson": lesson is not None,
                "lesson_path": lesson_path,
                "problems": [],
            }
            found = [parse_problem(p) for p in topic_dir.glob("*.py")
                     if p.name != "lesson.py" and not p.name.startswith("_")]
            found.sort(key=lambda p: (rank[p["difficulty"]], p["title"].lower()))
            for index, p in enumerate(found):
                p.update(topic_id=topic["id"], topic=topic["title"], index=index, of=len(found))
                problems[p["name"]] = p
                topic["problems"].append(p["name"])
            topics[topic["id"]] = topic
            stage["topics"].append(topic["id"])
    return stages, topics, problems


def all_problems():
    return load_course()[2]


def all_examples():
    examples = {}
    for folder in EXAMPLE_DIRS:
        for path in sorted((ROOT / folder).glob("*.py")):
            if path.name.startswith("_"):
                continue
            doc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or path.stem
            title = doc.strip().splitlines()[0].split("—")[0].split(",")[0].strip().rstrip(".")
            examples[f"{folder}/{path.stem}"] = {"id": f"{folder}/{path.stem}", "group": folder,
                                                 "title": title, "path": path}
    return examples


def load_progress():
    try:
        progress = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        progress = {}
    progress.setdefault("problems", {})
    progress.setdefault("lessons", {})
    return progress


PROGRESS_LOCK = threading.Lock()


def update_progress(change):
    with PROGRESS_LOCK:
        progress = load_progress()
        change(progress)
        WORKSPACE.mkdir(exist_ok=True)
        PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")
        return progress


def record_result(name, passed, total):
    def change(progress):
        best = progress["problems"].get(name, {}).get("solved", False)
        progress["problems"][name] = {"passed": passed, "total": total,
                                      "solved": best or (total > 0 and passed == total)}
    return update_progress(change)


def record_lesson_visit(topic_id):
    return update_progress(lambda progress: progress["lessons"].__setitem__(topic_id, True))


def saved_code_path(name):
    return WORKSPACE / "problems" / f"{name}.py"


# ── Running things ───────────────────────────────────────────────────────────

def docker_problem():
    """None if Docker is usable, otherwise a message the page can show."""
    DOCKER.refresh()
    state = DOCKER.state
    if state == "ready":
        return None
    return {
        "missing": "Docker isn't installed. Install Docker Desktop, then restart this server.",
        "stopped": "Docker Desktop isn't running. Start it, wait for it to say it's running, then press Run again.",
        "building": "The Python container image is still being prepared. Try again in a few seconds.",
        "broken": "The container image failed to build:\n" + DOCKER.detail,
    }.get(state, "Docker isn't ready yet.")


def run_tests(problem, code, custom=""):
    job = {"mode": "test", "name": problem["name"], "problem": problem["source"], "code": code, "custom": custom}
    run = run_in_container(job, TEST_DEADLINE)
    reply = {"container": run["container"], "seconds": run["seconds"]}
    if MARK in run["stdout"]:
        reply["report"] = json.loads(run["stdout"].rsplit(MARK, 1)[1])
    else:
        reply["crash"] = run["killed"] or (run["stderr"] or run["stdout"] or "The container exited unexpectedly.").strip()
    return reply


def run_script(code):
    run = run_in_container({"mode": "run", "code": code}, SCRIPT_DEADLINE)
    return {"container": run["container"], "seconds": run["seconds"], "exit_code": run["exit_code"],
            "output": run["stdout"] + run["stderr"], "killed": run["killed"]}


# ── HTTP ─────────────────────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):
    server_version = "DSAPlayground/1.0"

    def log_message(self, fmt, *args):
        if "/api/run" in self.path or (args and str(args[1]).startswith(("4", "5"))):
            sys.stderr.write(f"  {self.command} {self.path} {args[1] if len(args) > 1 else ''}\n")

    # helpers
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
        if WEB not in path.parents or not path.is_file():
            return self.fail("Not found", HTTPStatus.NOT_FOUND)
        types = {".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml"}
        data = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", types.get(path.suffix, "application/octet-stream") + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(data)

    # routes
    def do_GET(self):
        url = urlparse(self.path)
        query = {k: v[0] for k, v in parse_qs(url.query).items()}
        route = url.path

        if route == "/api/state":
            DOCKER.refresh_in_background()
            stages, topics, problems = load_course()
            return self.send_json({
                "docker": DOCKER.status(),
                "stages": stages,
                "topics": {tid: {k: v for k, v in t.items() if k != "lesson_path"} for tid, t in topics.items()},
                "problems": {name: {k: p[k] for k in ("name", "title", "difficulty", "topic_id", "tests")}
                             for name, p in problems.items()},
                "examples": [{k: e[k] for k in ("id", "group", "title")} for e in all_examples().values()],
                "progress": load_progress(),
            })

        if route == "/api/problem":
            problem = all_problems().get(query.get("name", ""))
            if not problem:
                return self.fail("Unknown problem", HTTPStatus.NOT_FOUND)
            saved = saved_code_path(problem["name"])
            data = {k: problem[k] for k in ("name", "title", "difficulty", "topic", "topic_id", "index", "of",
                                             "statement", "starter", "tests", "has_solution")}
            data["code"] = saved.read_text(encoding="utf-8") if saved.exists() else problem["starter"]
            return self.send_json(data)

        if route == "/api/lesson":
            topic = load_course()[1].get(query.get("topic", ""))
            if not topic or not topic["has_lesson"]:
                return self.fail("Unknown lesson", HTTPStatus.NOT_FOUND)
            lesson = parse_lesson(topic["lesson_path"])
            return self.send_json({"topic_id": topic["id"], "number": topic["number"], "title": topic["title"],
                                   "stage": topic["stage"], "notes": lesson["notes"], "code": lesson["code"],
                                   "problems": topic["problems"]})

        if route == "/api/solution":
            problem = all_problems().get(query.get("name", ""))
            if not problem or not problem["has_solution"]:
                return self.fail("No reference solution", HTTPStatus.NOT_FOUND)
            return self.send_json({"code": (SOLUTIONS / f"{problem['name']}.py").read_text(encoding="utf-8")})

        if route == "/api/example":
            example = all_examples().get(query.get("id", ""))
            if not example:
                return self.fail("Unknown example", HTTPStatus.NOT_FOUND)
            return self.send_json({"id": example["id"], "title": example["title"],
                                   "code": example["path"].read_text(encoding="utf-8")})

        if route == "/api/scratch":
            code = SCRATCH_FILE.read_text(encoding="utf-8") if SCRATCH_FILE.exists() else SCRATCH_STARTER
            return self.send_json({"code": code})

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

        if route == "/api/save":
            if data.get("kind") == "scratch":
                WORKSPACE.mkdir(exist_ok=True)
                SCRATCH_FILE.write_text(code, encoding="utf-8")
                return self.send_json({"saved": True})
            if data.get("name") in all_problems():
                path = saved_code_path(data["name"])
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(code, encoding="utf-8")
                return self.send_json({"saved": True})
            return self.fail("Unknown problem")

        if route == "/api/visit":
            if data.get("topic") not in load_course()[1]:
                return self.fail("Unknown topic")
            return self.send_json({"progress": record_lesson_visit(data["topic"])})

        if route == "/api/reset":
            problem = all_problems().get(data.get("name", ""))
            if data.get("kind") == "scratch":
                SCRATCH_FILE.unlink(missing_ok=True)
                return self.send_json({"code": SCRATCH_STARTER})
            if not problem:
                return self.fail("Unknown problem")
            saved_code_path(problem["name"]).unlink(missing_ok=True)
            return self.send_json({"code": problem["starter"]})

        if route == "/api/run":
            blocked = docker_problem()
            if blocked:
                return self.send_json({"docker_error": blocked, "docker": DOCKER.status()})
            kind = data.get("kind")
            if kind == "problem":
                problem = all_problems().get(data.get("name", ""))
                if not problem:
                    return self.fail("Unknown problem")
                path = saved_code_path(problem["name"])
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(code, encoding="utf-8")
                reply = run_tests(problem, code, str(data.get("custom") or "")[:2000])
                tests = reply.get("report", {}).get("tests", [])
                if tests and not all(t["status"] == "todo" for t in tests):
                    record_result(problem["name"], sum(t["status"] == "pass" for t in tests), len(tests))
                reply["progress"] = load_progress()
                return self.send_json(reply)
            if kind in ("scratch", "example", "lesson"):
                if kind == "scratch":
                    WORKSPACE.mkdir(exist_ok=True)
                    SCRATCH_FILE.write_text(code, encoding="utf-8")
                return self.send_json(run_script(code))
            return self.fail("Unknown kind of run")

        self.fail("Not found", HTTPStatus.NOT_FOUND)


# ── Self-check ───────────────────────────────────────────────────────────────

def check():
    """Every reference solution must pass, every untouched stub must report 'todo',
    and every example must run cleanly — all inside real containers."""
    print("Preparing the container image...")
    DOCKER.refresh()
    if DOCKER.state != "ready":
        print(docker_problem())
        return 1
    failures = 0
    for problem in all_problems().values():
        solution = (SOLUTIONS / f"{problem['name']}.py").read_text(encoding="utf-8")
        reply = run_tests(problem, solution)
        tests = reply.get("report", {}).get("tests", [])
        ok = tests and all(t["status"] == "pass" for t in tests)
        stub = run_tests(problem, problem["starter"])
        stub_ok = all(t["status"] == "todo" for t in stub.get("report", {}).get("tests", [{"status": "?"}]))
        mark = "ok  " if ok and stub_ok else "FAIL"
        failures += not (ok and stub_ok)
        print(f"  {mark} {problem['name']:<30} {len(tests)} tests  {reply['seconds']}s")
        if not ok:
            print("       ", json.dumps(reply)[:1500])
        if not stub_ok:
            print("        starter code didn't report 'todo':", json.dumps(stub)[:800])
    scripts = [(f"lesson {t['id']}", parse_lesson(t["lesson_path"])["code"])
               for t in load_course()[1].values() if t["has_lesson"]]
    scripts += [(f"example {e['id']}", e["path"].read_text(encoding="utf-8")) for e in all_examples().values()]
    for label, code in scripts:
        run = run_script(code)
        ok = run["exit_code"] == 0
        failures += not ok
        print(f"  {'ok  ' if ok else 'FAIL'} {label:<48} {run['seconds']}s")
        if not ok:
            print("       ", run["output"][-1500:], run["killed"] or "")
    missing = [t["id"] for t in load_course()[1].values() if not t["has_lesson"]]
    if missing:
        failures += len(missing)
        print("  FAIL topics without a lesson.py:", ", ".join(missing))
    print("\nAll good." if not failures else f"\n{failures} problem(s).")
    return 1 if failures else 0


def main():
    parser = argparse.ArgumentParser(description="DSA Playground")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-browser", action="store_true", help="don't open a browser tab")
    parser.add_argument("--check", action="store_true", help="verify solutions, stubs and examples in containers")
    args = parser.parse_args()

    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    if args.check:
        return check()

    DOCKER.refresh_in_background()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)  # local only: it runs code
    url = f"http://localhost:{args.port}"
    print(f"\n  DSA Playground running at {url}")
    print("  Each Run starts a fresh Docker container. Press Ctrl+C to stop.\n")
    if not args.no_browser:
        threading.Timer(0.6, webbrowser.open, [url]).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Stopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
