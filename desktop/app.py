"""
Trace desktop app: the same course and IDE, in its own window, with no Docker and no browser.

    python desktop/app.py        run from source (needs: pip install pywebview)
    Trace.exe                    the packaged app (see desktop/build.py)

The local server listens on a random port on 127.0.0.1 only, and stops when the window closes.
Code runs in the bundled Python (runtime/python) as a separate, limited process per Run.
"""
import os
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

if not getattr(sys, "frozen", False):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))     # import server.py from the project root

import server  # noqa: E402

DATA_DIR = Path(os.environ.get("LOCALAPPDATA") or Path.home()) / "Trace"


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def open_in_edge_app_mode(url):
    """Fallback window: Edge's chromeless app mode, with its own profile. Blocks until it's closed."""
    candidates = [Path(os.environ.get(v, "")) / "Microsoft/Edge/Application/msedge.exe"
                  for v in ("ProgramFiles(x86)", "ProgramFiles", "LOCALAPPDATA")]
    edge = next((p for p in candidates if p.exists()), None)
    if not edge:
        import webbrowser
        webbrowser.open(url)
        input("Trace is open in your browser. Press Enter here to quit.\n")
        return
    profile = DATA_DIR / "edge-profile"
    proc = subprocess.Popen([str(edge), f"--app={url}", f"--user-data-dir={profile}", "--no-first-run",
                             "--window-size=1360,880"])
    proc.wait()


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    port = free_port()
    httpd = server.start_server("127.0.0.1", port)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{port}/?app=1"
    try:
        import webview
    except ImportError:
        webview = None
    try:
        if webview is None:
            raise RuntimeError("pywebview is not installed")
        webview.create_window("Trace", url, width=1360, height=880, min_size=(1024, 680),
                              background_color="#ffffff", text_select=True)
        # private_mode=False keeps localStorage (drill progress, theme, panel sizes) between launches.
        webview.start(private_mode=False, storage_path=str(DATA_DIR / "webview"))
    except Exception as exc:  # noqa: BLE001 - e.g. WebView2 missing: fall back to Edge app mode
        sys.stderr.write(f"Native window unavailable ({exc}); using Edge app mode.\n")
        open_in_edge_app_mode(url)
    finally:
        httpd.shutdown()
        time.sleep(0.1)


if __name__ == "__main__":
    main()
