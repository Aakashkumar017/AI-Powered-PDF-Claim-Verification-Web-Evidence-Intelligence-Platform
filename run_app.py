"""
GEO Fact Checker — Application Launcher
Run:  python run_app.py
"""

import subprocess
import time
import os
import sys
import webbrowser
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────────

BACKEND_PORT  = 8000
FRONTEND_PORT = 8501
PROJECT_ROOT  = Path(__file__).parent

# ── PYTHON EXECUTABLE ─────────────────────────────────────────────────────────

def get_python() -> str:
    venv = (
        PROJECT_ROOT / "venv" / ("Scripts" if os.name == "nt" else "bin") / (
            "python.exe" if os.name == "nt" else "python"
        )
    )
    return str(venv) if venv.exists() else sys.executable


PYTHON = get_python()

# ── HELPERS ───────────────────────────────────────────────────────────────────

def _line():    print("=" * 70)
def _ok(msg):   print(f"[ OK  ] {msg}")
def _err(msg):  print(f"[FAIL] {msg}")
def _info(msg): print(f"[INFO] {msg}")

# ── INSTALL DEPENDENCIES ──────────────────────────────────────────────────────

def install_dependencies():
    _line(); _info("Installing dependencies"); _line()
    for label, req in [
        ("backend",  PROJECT_ROOT / "backend"  / "requirements.txt"),
        ("frontend", PROJECT_ROOT / "frontend" / "requirements.txt"),
    ]:
        try:
            subprocess.check_call(
                [PYTHON, "-m", "pip", "install", "-r", str(req)],
                stdout=subprocess.DEVNULL,
            )
            _ok(f"{label} packages installed")
        except subprocess.CalledProcessError as e:
            _err(f"{label} install failed: {e}")

# ── START BACKEND ─────────────────────────────────────────────────────────────

def start_backend() -> subprocess.Popen:
    _line(); _info("Starting FastAPI backend"); _line()
    return subprocess.Popen(
        [PYTHON, "-m", "uvicorn", "app.main:app",
         "--reload", "--host", "0.0.0.0", "--port", str(BACKEND_PORT)],
        cwd=str(PROJECT_ROOT / "backend"),
    )

# ── WAIT FOR BACKEND ──────────────────────────────────────────────────────────

def wait_for_backend(timeout: int = 30) -> bool:
    _info("Waiting for backend …")
    # Import requests lazily so the launcher works before install too
    try:
        import requests as _req
    except ImportError:
        _err("'requests' not installed — cannot probe backend.")
        return False

    url = f"http://127.0.0.1:{BACKEND_PORT}/"
    for _ in range(timeout):
        try:
            _req.get(url, timeout=1)
            _ok("Backend is up")
            return True
        except Exception:
            time.sleep(1)
    _err("Backend did not start in time.")
    return False

# ── START FRONTEND ────────────────────────────────────────────────────────────

def start_frontend() -> subprocess.Popen:
    _line(); _info("Starting Streamlit frontend"); _line()
    return subprocess.Popen(
        [PYTHON, "-m", "streamlit", "run", "app.py",
         "--server.port", str(FRONTEND_PORT),
         "--server.headless", "true"],
        cwd=str(PROJECT_ROOT / "frontend"),
    )

# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    _line(); print("  GEO FACT CHECKER"); _line()
    os.chdir(PROJECT_ROOT)

    install_dependencies()

    backend_proc  = start_backend()
    if not wait_for_backend():
        backend_proc.terminate()
        return

    frontend_proc = start_frontend()

    # Give Streamlit a few seconds to bind its port before opening the browser
    time.sleep(5)
    url = f"http://localhost:{FRONTEND_PORT}"
    _info(f"Opening browser: {url}")
    webbrowser.open(url)

    _line()
    _ok("Application running")
    print(f"  Frontend : {url}")
    print(f"  Backend  : http://localhost:{BACKEND_PORT}")
    print(f"  Swagger  : http://localhost:{BACKEND_PORT}/docs")
    print("  Press Ctrl+C to stop.")
    _line()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        _info("Shutting down …")
        backend_proc.terminate()
        frontend_proc.terminate()
        _ok("Done.")


if __name__ == "__main__":
    main()