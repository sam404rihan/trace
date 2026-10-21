"""
Runs inside a brand-new container for every Run. Reads one JSON job from stdin.

    {"mode": "run",  "code": "..."}
        Execute the code as a normal script. Output goes straight to stdout.

    {"mode": "test", "name": "two_sum", "problem": "<problem file>", "code": "...", "custom": "two_sum([1, 2], 3)", "upto": 2}
        Load the user's code, run it against the problem's tests, and print one
        JSON result after the MARK line.

Problem files can define:
    TESTS = [((args...), expected), ...]           plain function tests
    STEPS = [{"title", "text", "hint", "tests"}]   guided problems; "upto" picks how many steps run
    CLASS = "LRUCache"                             tests are call sequences:
                                                   ([("LRUCache", 2), ("put", 1, 1), ("get", 1)], [None, None, 1])
    PREPARE(*args) -> args, FINISH(value) -> value, CHECK(got, expected[, args]) -> bool
"""
import inspect
import copy
import json
import signal
import sys
import time
import traceback
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

import os

# runner/ (prelude) and the project root (helpers, structures, algorithms). Set here rather than via
# PYTHONPATH, because the bundled embeddable Python ignores PYTHONPATH.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [_HERE, os.path.dirname(_HERE)]

from prelude import PRELUDE   # noqa: E402 - names available to user code without importing (runner/prelude.py)

MARK = "@@DSA_RESULT@@"
TEST_TIMEOUT = 2.0      # seconds per test
LOAD_TIMEOUT = 3.0      # seconds to run the top level of the user's file
SCRIPT_TIMEOUT = 10.0   # seconds for a plain "run"
OUTPUT_LIMIT = 20_000   # characters of printed output kept per test


class Timeout(BaseException):
    """BaseException, so a bare `except Exception` in user code can't swallow it."""


if hasattr(signal, "setitimer"):
    # Unix: an exact interval timer.
    def _on_alarm(signum, frame):
        raise Timeout()

    signal.signal(signal.SIGALRM, _on_alarm)

    def alarm(seconds):
        """Raise Timeout in this thread after `seconds` (0 cancels)."""
        signal.setitimer(signal.ITIMER_REAL, seconds)
else:
    # Windows has no SIGALRM. A watchdog thread interrupts the main thread instead, through a
    # SIGINT handler that only raises Timeout while a limit is armed (a late interrupt is ignored).
    import _thread
    import threading

    _armed = {"token": 0, "on": False}
    _timer = [None]

    def _on_interrupt(signum, frame):
        if _armed["on"]:
            _armed["on"] = False
            raise Timeout()

    signal.signal(signal.SIGINT, _on_interrupt)

    def alarm(seconds):
        """Raise Timeout in the main thread after `seconds` (0 cancels)."""
        _armed["token"] += 1
        _armed["on"] = False
        if _timer[0]:
            _timer[0].cancel()
            _timer[0] = None
        if seconds <= 0:
            return
        token = _armed["token"]
        _armed["on"] = True

        def fire():
            if _armed["on"] and _armed["token"] == token:
                _thread.interrupt_main()

        _timer[0] = threading.Timer(seconds, fire)
        _timer[0].daemon = True
        _timer[0].start()


def clip(text, limit=OUTPUT_LIMIT):
    return text if len(text) <= limit else text[:limit] + f"\n... ({len(text) - limit:,} more characters cut)"


def short_repr(value, limit=160):
    text = repr(value)
    return text if len(text) <= limit else text[: limit - 3] + "..."


def user_traceback(exc, filename):
    """Keep only the frames from the user's own file, so the error points at their code."""
    frames = [f for f in traceback.extract_tb(exc.__traceback__) if f.filename == filename]
    if not frames:
        frames = [f for f in traceback.extract_tb(exc.__traceback__) if not f.filename.endswith("judge.py")]
    lines = traceback.format_list(frames) + traceback.format_exception_only(type(exc), exc)
    return "".join(lines).rstrip()


def guarded(fn, timeout):
    """Call fn() with a time limit, capturing everything it prints."""
    out = StringIO()
    result = {"value": None, "exc": None, "timed_out": False}
    start = time.perf_counter()
    alarm(timeout)
    try:
        with redirect_stdout(out), redirect_stderr(out):
            result["value"] = fn()
    except Timeout:
        result["timed_out"] = True
    except BaseException as exc:  # noqa: BLE001 - report whatever the user's code raises
        result["exc"] = exc
    finally:
        alarm(0)
    result["ms"] = (time.perf_counter() - start) * 1000
    result["output"] = clip(out.getvalue())
    return result


def run_script(job):
    sys.stderr = sys.stdout  # keep prints and errors in the order they happened
    namespace = {"__name__": "__main__", **PRELUDE}
    alarm(SCRIPT_TIMEOUT)
    try:
        exec(compile(job["code"], "main.py", "exec"), namespace)
    except Timeout:
        print(f"\n[stopped: still running after {SCRIPT_TIMEOUT:g} seconds — an infinite loop?]")
        return 1
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 0
    except BaseException as exc:  # noqa: BLE001
        print(user_traceback(exc, "main.py"))
        return 1
    finally:
        alarm(0)
    return 0


def explain_mismatch(got, expected):
    """A plain-language hint for the common near-misses, so nobody has to diff two lists by eye."""
    try:
        if isinstance(got, (list, tuple)) and isinstance(expected, (list, tuple)):
            if len(got) == len(expected) and sorted(map(repr, got)) == sorted(map(repr, expected)):
                return ("Right items, wrong order. Every element is correct, only the order differs. "
                        "Check the ordering rule in the statement (for example, how ties are broken).")
            if set(map(repr, got)) == set(map(repr, expected)):
                return "Same distinct items, but some appear the wrong number of times (missing or duplicated)."
            if len(got) != len(expected):
                return f"Expected {len(expected)} item{'s' if len(expected) != 1 else ''}, got {len(got)}."
        if isinstance(got, type(expected)) is False and expected is not None and got is not None:
            return f"Expected a {type(expected).__name__}, got a {type(got).__name__}."
        if got is None and expected is not None:
            return "Your function returned None. Is a `return` missing?"
        if isinstance(got, float) and isinstance(expected, float) and abs(got - expected) < 0.01:
            return "Very close. Check the rounding the statement asks for."
    except BaseException:  # noqa: BLE001 - hints are best-effort (FINISH may fail on a bad value)
        pass
    return None


def run_class_test(cls, calls, expected, test, finish):
    """Replay a sequence of calls: the first builds the object, the rest are method calls."""
    got = []

    def replay():
        obj = cls(*copy.deepcopy(calls[0][1:]))
        got.append(None)
        for method, *args in calls[1:]:
            value = getattr(obj, method)(*copy.deepcopy(args))
            got.append(finish(value) if finish else value)
        return got

    ran = guarded(replay, TEST_TIMEOUT)
    test["ms"] = round(ran["ms"], 2)
    test["output"] = ran["output"]
    if ran["timed_out"]:
        test["status"] = "timeout"
        test["error"] = f"Still running after {TEST_TIMEOUT:g}s. An infinite loop, or too slow for this input?"
        return
    if isinstance(ran["exc"], NotImplementedError):
        test["status"] = "todo"
        return
    if ran["exc"]:
        where = calls[len(got)] if len(got) < len(calls) else calls[-1]
        test["status"] = "error"
        call = f"{where[0]}({', '.join(short_repr(a, 40) for a in where[1:])})"
        test["error"] = f"During {call}:\n" + user_traceback(ran["exc"], "solution.py")
        return
    test["got"] = short_repr(got, 400)
    if got == expected:
        test["status"] = "pass"
        return
    test["status"] = "fail"
    for i, (g, e) in enumerate(zip(got, expected)):
        if g != e:
            c = calls[i]
            test["error"] = f"Call {i + 1}, {c[0]}({', '.join(short_repr(a, 40) for a in c[1:])}): returned {short_repr(g)}, expected {short_repr(e)}"
            break


def _no_recursion_limit(limit):
    raise RuntimeError("sys.setrecursionlimit is switched off in the judge: tests run with Python's normal "
                       "recursion limit (about 1,000 calls deep). If a test is too deep for recursion, "
                       "use an explicit stack or a loop instead.")


def run_tests(job):
    name = job["name"]
    report = {"tests": [], "load_error": None, "load_output": "", "custom": None}

    problem = {"__name__": "problem"}
    exec(compile(job["problem"], "problem.py", "exec"), problem)
    # Deep tests teach the explicit stack, so a solution can't raise the limit to get past them.
    sys.setrecursionlimit = _no_recursion_limit

    solution = {"__name__": "solution", **PRELUDE}   # collections, heapq, bisect, ... without imports
    loaded = guarded(lambda: exec(compile(job["code"], "solution.py", "exec"), solution), LOAD_TIMEOUT)
    report["load_output"] = loaded["output"]
    if loaded["timed_out"]:
        report["load_error"] = f"Your file took longer than {LOAD_TIMEOUT:g}s just to load. Is there a loop outside the function?"
        return report
    if loaded["exc"]:
        report["load_error"] = user_traceback(loaded["exc"], "solution.py")
        return report
    cls_name = problem.get("CLASS")
    target = cls_name or name
    fn = solution.get(target)
    if fn is PRELUDE.get(target):       # e.g. itertools.combinations, when the user's own def is missing
        fn = None
    if not callable(fn):
        what = "class" if cls_name else "function"
        report["load_error"] = f"Couldn't find a {what} called `{target}`. Keep the name from the starter code."
        return report

    prepare = problem.get("PREPARE")
    finish = problem.get("FINISH")
    check = problem.get("CHECK")
    check_args = bool(check) and len(inspect.signature(check).parameters) >= 3

    if problem.get("STEPS"):
        upto = max(1, min(int(job.get("upto") or len(problem["STEPS"])), len(problem["STEPS"])))
        cases = [(i, t) for i, st in enumerate(problem["STEPS"][:upto]) for t in st["tests"]]
    else:
        cases = [(None, t) for t in problem.get("TESTS", [])]

    timeouts = 0
    for step, (args, expected) in cases:
        if cls_name:
            test = {"call": "; ".join(f"{c[0]}({', '.join(short_repr(a, 40) for a in c[1:])})" for c in args)[:400],
                    "expected": short_repr(expected, 400)}
        else:
            test = {"call": f"{name}({', '.join(short_repr(a, 60) for a in args)})", "expected": short_repr(expected)}
        if step is not None:
            test["step"] = step
        report["tests"].append(test)
        if timeouts >= 2:  # it's almost certainly an infinite loop; don't make them wait for every test
            test["status"] = "skipped"
            continue
        if cls_name:
            run_class_test(fn, args, expected, test, finish)
            if test["status"] == "timeout":
                timeouts += 1
            continue
        call_args = copy.deepcopy(args)
        if prepare:
            try:
                call_args = prepare(*call_args)
            except Exception as exc:  # noqa: BLE001 - a broken PREPARE in the problem file
                test["status"], test["error"] = "error", "The problem's PREPARE failed:\n" + user_traceback(exc, "problem.py")
                continue
        ran = guarded(lambda: fn(*call_args), TEST_TIMEOUT)
        test["ms"] = round(ran["ms"], 2)
        test["output"] = ran["output"]
        if ran["timed_out"]:
            timeouts += 1
            test["status"] = "timeout"
            test["error"] = f"Still running after {TEST_TIMEOUT:g}s. An infinite loop, or too slow for this input?"
        elif isinstance(ran["exc"], NotImplementedError):
            test["status"] = "todo"
        elif ran["exc"]:
            test["status"] = "error"
            test["error"] = user_traceback(ran["exc"], "solution.py")
        else:
            try:
                got = finish(ran["value"]) if finish else ran["value"]
                test["got"] = short_repr(got)
                if check_args:
                    ok = bool(check(got, expected, copy.deepcopy(args)))
                else:
                    ok = bool(check(got, expected)) if check else got == expected
            except Exception:  # noqa: BLE001 - e.g. CHECK tried to sort a None
                test["got"] = short_repr(ran["value"])
                ok = False
            test["status"] = "pass" if ok else "fail"
            if not ok and not check:            # with a custom CHECK, "expected" is only a description
                try:
                    shown = finish(ran["value"]) if finish else ran["value"]
                except Exception:  # noqa: BLE001
                    shown = ran["value"]
                test["note"] = explain_mismatch(shown, expected)

    expr = (job.get("custom") or "").strip()
    if expr:
        env = dict(solution)                             # prelude + everything the user defined
        ran = guarded(lambda: eval(compile(expr, "your call", "eval"), env), TEST_TIMEOUT)
        custom = {"expr": expr, "output": ran["output"]}
        if ran["timed_out"]:
            custom["error"] = f"Still running after {TEST_TIMEOUT:g}s."
        elif ran["exc"]:
            custom["error"] = user_traceback(ran["exc"], "solution.py")
        else:
            custom["value"] = short_repr(ran["value"], 2000)
        report["custom"] = custom
    return report


def main():
    job = json.loads(sys.stdin.read())
    if job["mode"] == "run":
        sys.exit(run_script(job))
    report = run_tests(job)
    sys.__stdout__.write("\n" + MARK + json.dumps(report) + "\n")


if __name__ == "__main__":
    main()
