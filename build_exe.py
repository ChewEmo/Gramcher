import os
import subprocess
import sys
from pathlib import Path

project_dir = Path(__file__).resolve().parent
python_exe = sys.executable

print("Installing PyInstaller...")
subprocess.check_call([python_exe, "-m", "pip", "install", "--user", "pyinstaller"], cwd=str(project_dir))

resources = [
    "background.png",
    "tubiao.ico",
    "zh_CN.json",
    "en_US.json",
    "fr_FR.json",
    "hi_IN.json",
    "ja_JP.json",
    "ru_RU.json",
]

cmd = [
    python_exe,
    "-m",
    "PyInstaller",
    "--noconsole",
    "--onefile",
    "--icon=tubiao.ico",
    "--name",
    "Gramcher",
]
for resource in resources:
    cmd.extend(["--add-data", f"{resource}{os.pathsep}."])
cmd.append("main.py")

print("Building EXE...")
subprocess.check_call(cmd, cwd=str(project_dir))

exe_path = project_dir / "dist" / "Gramcher.exe"
print(f"EXE built at: {exe_path}")
print("Exists:", exe_path.exists())
