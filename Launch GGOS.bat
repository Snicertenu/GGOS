@echo off
echo Starting GGOS - Get Good or Swole...
echo.
cd /d "%~dp0"
if exist "dist\GGOS.exe" (
    start "" "dist\GGOS.exe"
) else (
    echo Error: GGOS.exe not found in dist folder
    echo Please run: python -m PyInstaller --onefile --windowed --name=GGOS main.py
    pause
)
