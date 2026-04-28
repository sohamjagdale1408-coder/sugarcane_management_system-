@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   Sugar Management System - Starting...
echo ========================================
echo.

:: Change to the script's directory
cd /d "%~dp0"

:: Check for Python
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

:: Install dependencies
echo.
echo Installing Flask and dependencies...
python -m pip install --upgrade pip
python -m pip install flask werkzeug

if %errorlevel% neq 0 (
    echo.
    echo WARNING: Dependency installation might have failed.
    echo Attempting to run anyway...
)

echo.
echo ========================================
echo  Starting server at http://127.0.0.1:5000
echo  Keep this window open!
echo ========================================
echo.

:: Run the application
python app.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Server failed to start. 
    echo Please check if port 5000 is already in use.
)

echo.
pause
