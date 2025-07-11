import atexit
import subprocess

import psutil
import requests


class PhosphoClient:
    BASE_URL = "http://localhost:80"

    def __init__(self):
        self._process = None
        atexit.register(self.stop)

    def start(self):
        if self._process is not None and self._process.poll() is None:
            print("[phosphobot] Already started (PID={})".format(self._process.pid))
            return
        print("[phosphobot] Starting...")
        self._process = subprocess.Popen(["phosphobot", "run"])
        print(f"[phosphobot] Started with PID={self._process.pid}")

    def stop(self):
        print("phosphobot: calling .stop()")
        found = False
        if self._process and self._process.poll() is None:
            try:
                proc = psutil.Process(self._process.pid)
                for child in proc.children(recursive=True):
                    print(f"[phosphobot] Killing child PID={child.pid}")
                    child.kill()
                print(f"[phosphobot] Killing main PID={proc.pid}")
                proc.kill()
                found = True
            except psutil.NoSuchProcess:
                pass
            self._process = None

        # Fallback: kill any remaining phosphobot processes by name
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmd = proc.info['cmdline']
                if cmd and any("phosphobot" in c for c in cmd):
                    print(f"[phosphobot] Force killing stray PID={proc.pid}")
                    proc.kill()
                    found = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if not found:
            print("[phosphobot] No process found to kill.")

    def post(self, endpoint: str, json: dict | None=None):
        # if self._process is None or self._process.poll() is not None:
        #     self.start()
        url = self.BASE_URL + endpoint
        try:
            response = requests.post(url, json=json)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[phosphobot] POST request failed: {e}")
            return {"status": "error", "error": str(e)}

    def get(self, endpoint: str, params: dict | None=None):
        # if self._process is None or self._process.poll() is not None:
        #     self.start()
        url = self.BASE_URL + endpoint
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[phosphobot] GET request failed: {e}")
            return {"status": "error", "error": str(e)}
