"""
Build the Trace desktop app for Windows.

    python desktop/build.py              build dist/Trace/Trace.exe
    python desktop/build.py --shortcut   ...and put a Trace shortcut on your desktop and in the Start menu

What it does:
  1. Makes a private build environment in .build-venv/ (PyInstaller, pywebview, Pillow).
  2. Downloads the official embeddable Python 3.14 into runtime/python if it's missing.
     That's the Python your code runs on inside the app.
  3. Draws the app icon and runs PyInstaller (one folder, no console window).
"""
import argparse
import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENV = ROOT / ".build-venv"
PY = VENV / "Scripts" / "python.exe"
RUNTIME = ROOT / "runtime" / "python"
EMBED_VERSION = "3.14.8"
ICON = ROOT / "desktop" / "trace.ico"

# Standard-library modules the course's problem files use when the app reads them.
STDLIB = ["random", "bisect", "heapq", "itertools", "functools", "collections", "math", "string", "re",
          "statistics", "fractions", "decimal", "copy", "typing", "operator", "inspect", "gzip", "uuid",
          "tempfile", "webbrowser", "ctypes", "ctypes.wintypes"]


def run(*cmd):
    print("  $", " ".join(map(str, cmd)))
    subprocess.check_call([str(c) for c in cmd], cwd=ROOT)


def ensure_venv():
    if not PY.exists():
        print("Creating the build environment...")
        run(sys.executable, "-m", "venv", VENV)
    run(PY, "-m", "pip", "install", "--quiet", "--upgrade", "pip", "pyinstaller", "pywebview", "pillow")


def ensure_runtime():
    if (RUNTIME / "python.exe").exists():
        return
    print(f"Downloading embeddable Python {EMBED_VERSION}...")
    RUNTIME.mkdir(parents=True, exist_ok=True)
    url = f"https://www.python.org/ftp/python/{EMBED_VERSION}/python-{EMBED_VERSION}-embed-amd64.zip"
    archive = RUNTIME.parent / "python-embed.zip"
    urllib.request.urlretrieve(url, archive)
    with zipfile.ZipFile(archive) as z:
        z.extractall(RUNTIME)
    archive.unlink()


def draw_icon():
    script = r'''
from PIL import Image, ImageDraw
import sys
big = 256
img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
d.rounded_rectangle((8, 8, big - 8, big - 8), radius=56, fill=(26, 26, 29, 255))
d.rounded_rectangle((64, 166, big - 64, 194), radius=14, fill=(255, 225, 122, 255))
img.save(sys.argv[1], sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
'''
    run(PY, "-c", script, ICON)


def build():
    sep = ";"
    datas = ["web", "course", "solutions", "runner", "structures", "algorithms", "runtime", "helpers.py"]
    args = [PY, "-m", "PyInstaller", "--noconfirm", "--clean", "--windowed", "--name", "Trace",
            "--icon", ICON, "--distpath", ROOT / "dist", "--workpath", ROOT / ".build-work",
            "--specpath", ROOT / ".build-work", "--paths", ROOT]
    for item in datas:
        dest = item if (ROOT / item).is_dir() else "."
        args += ["--add-data", f"{ROOT / item}{sep}{dest}"]
    for mod in STDLIB:
        args += ["--hidden-import", mod]
    args.append(ROOT / "desktop" / "app.py")
    run(*args)


def make_shortcuts():
    exe = ROOT / "dist" / "Trace" / "Trace.exe"
    targets = [Path(os.environ["USERPROFILE"]) / "Desktop" / "Trace.lnk",
               Path(os.environ["APPDATA"]) / "Microsoft/Windows/Start Menu/Programs/Trace.lnk"]
    for lnk in targets:
        ps = (f"$s=(New-Object -ComObject WScript.Shell).CreateShortcut('{lnk}');"
              f"$s.TargetPath='{exe}';$s.WorkingDirectory='{exe.parent}';$s.IconLocation='{exe},0';$s.Save()")
        subprocess.check_call(["powershell", "-NoProfile", "-Command", ps])
        print("  shortcut:", lnk)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shortcut", action="store_true", help="add Desktop and Start-menu shortcuts")
    args = parser.parse_args()
    ensure_venv()
    ensure_runtime()
    draw_icon()
    if (ROOT / "dist" / "Trace").exists():
        shutil.rmtree(ROOT / "dist" / "Trace")
    build()
    print("\nBuilt:", ROOT / "dist" / "Trace" / "Trace.exe")
    if args.shortcut:
        make_shortcuts()


if __name__ == "__main__":
    main()
