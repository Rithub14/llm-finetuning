import subprocess
import sys
import os

def start_streamlit():
    frontend_path = os.path.abspath("frontend/app.py")

    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        frontend_path,
        "--server.port=8001",
        "--server.headless=true",
    ]

    subprocess.Popen(cmd)
