"""Desktop entry point: start the backend and open the app in the browser.

Run with pythonw.exe (no console window). The backend serves the built
frontend itself, so this single process is the whole app.
"""
import os
import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path

# Under pythonw there is no console; give the app a log file instead.
if sys.stdout is None or sys.stderr is None:
    log_dir = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "SmartCCTV" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = open(log_dir / "app.log", "a", encoding="utf-8")
    if sys.stdout is None:
        sys.stdout = log_file
    if sys.stderr is None:
        sys.stderr = log_file

BACKEND_DIR = Path(__file__).resolve().parent / "backend"
HOST = "127.0.0.1"


def _port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((HOST, port)) == 0


def main() -> None:
    os.chdir(BACKEND_DIR)
    sys.path.insert(0, str(BACKEND_DIR))

    from utils.config import settings

    url = f"http://{HOST}:{settings.PORT}"

    if _port_in_use(settings.PORT):
        print(f"[launcher] SmartCCTV already running on port {settings.PORT}; opening {url}")
        webbrowser.open(url)
        return

    import uvicorn
    from main import app

    print(f"[launcher] Starting SmartCCTV on {url}")
    server = uvicorn.Server(
        uvicorn.Config(app, host=HOST, port=settings.PORT, log_level=settings.LOG_LEVEL.lower())
    )

    def open_when_ready():
        while not server.started:
            time.sleep(0.2)
        webbrowser.open(url)

    threading.Thread(target=open_when_ready, daemon=True).start()
    server.run()


if __name__ == "__main__":
    main()
