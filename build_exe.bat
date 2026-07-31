@echo off
setlocal
cd /d "%~dp0"
"B:/Python 3.14.6/python.exe" -m pip install --user pyinstaller
"B:/Python 3.14.6/python.exe" -m PyInstaller --noconsole --onefile --icon=tubiao.ico --name Gramcher --add-data "background.png;." --add-data "tubiao.ico;." --add-data "zh_CN.json;." --add-data "en_US.json;." --add-data "fr_FR.json;." --add-data "hi_IN.json;." --add-data "ja_JP.json;." --add-data "ru_RU.json;." main.py
endlocal
