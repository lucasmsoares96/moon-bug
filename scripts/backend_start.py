import subprocess
import sys
import os
import platform
import socket

project = os.getenv("MOON_PROJECT_ID", "app").replace("-backend", "")

wait = ["--wait-for-client"] if "--wait" in sys.argv else []

PORTS_TO_FREE = [5678, 4001, 4002]


def free_port(port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("127.0.0.1", port)) != 0:
            return
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["netstat", "-ano"], capture_output=True, text=True
            )
            for line in result.stdout.splitlines():
                if f":{port}" in line and "LISTENING" in line:
                    pid = line.strip().split()[-1]
                    print(f"Killing zombie process on port {port} (PID: {pid})")
                    subprocess.run(
                        ["taskkill", "/F", "/T", "/PID", pid], capture_output=True
                    )
        else:
            result = subprocess.run(
                ["lsof", "-ti", f":{port}"], capture_output=True, text=True
            )
            for pid in result.stdout.split():
                print(f"Killing zombie process on port {port} (PID: {pid})")
                subprocess.run(["kill", "-9", pid], capture_output=True)
    except Exception as e:
        print(f"Warning: Could not kill process on port {port}: {e}")


for port in PORTS_TO_FREE:
    free_port(port)

cmd = [
    "uv",
    "run",
    "--env-file",
    ".env",
    "--",
    "python",
    "-Xfrozen_modules=off",
    "-m",
    "debugpy",
    "--listen",
    "0.0.0.0:5678",
    *wait,
    "-m",
    "uvicorn",
    f"{project}.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "4002",
    "--reload",
    "--reload-dir",
    ".",
    "--reload-dir",
    "../../packages",
]

try:
    subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as e:
    print(f"Backend process failed with exit code {e.returncode}")
    sys.exit(e.returncode)
except KeyboardInterrupt:
    pass
