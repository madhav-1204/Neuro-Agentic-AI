@echo off
title Neuro Diagnosis App

echo ========================================
echo   Starting Neuro Diagnosis App
echo ========================================
echo.

:: Start Backend
echo [1/2] Starting Backend...
start "Backend - Neuro Diagnosis" cmd /k "cd /d b:\testp\backend && pip install -r requirements.txt && uvicorn main:app --reload"

:: Wait a moment for backend to initialize
timeout /t 3 /nobreak >nul

:: Start Frontend
echo [2/2] Starting Frontend...
start "Frontend - Neuro Diagnosis" cmd /k "cd /d b:\testp\frontend && npm install && npm run dev"

echo.
echo ========================================
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo ========================================
echo.
echo Close the terminal windows to stop.
pause
