@echo off
echo Starting Hospital OpenEnv API Server...
echo.
echo Server will start on: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
cd /d "%~dp0"
python main.py
pause
