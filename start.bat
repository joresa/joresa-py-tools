@echo off
REM Joresa Tools - Quick Start Script for Windows
REM This script sets up and runs both backend and frontend

echo Starting Joresa Tools...

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3 first.
    exit /b 1
)

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo Node.js is not installed. Please install Node.js first.
    exit /b 1
)

REM Setup backend
echo Setting up backend...
cd backend
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -q -r requirements.txt

REM Start backend
echo Starting backend server on http://localhost:8000...
start /B python main.py
cd ..

REM Setup frontend
echo Setting up frontend...
cd frontend
if not exist "node_modules" (
    call npm install
)

REM Start frontend
echo Starting frontend on http://localhost:5173...
start /B npm run dev
cd ..

echo.
echo Joresa Tools is running!
echo.
echo Dashboard: http://localhost:5173
echo API: http://localhost:8000
echo.
echo Press Ctrl+C to stop...

pause
