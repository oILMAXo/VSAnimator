@echo off
chcp 65001 >nul 2>&1
title VS Animator

echo ============================================
echo   VS Animator - Vintage Story Editor
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [!] Python не найден / Python not found
        echo     Скачайте: https://www.python.org/downloads/
        echo     Download: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    set PY=py
) else (
    set PY=python
)

:: Install pywebview if needed
%PY% -c "import webview" >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Установка pywebview / Installing pywebview...
    %PY% -m pip install pywebview --quiet
    if %errorlevel% neq 0 (
        echo [!] Ошибка установки / Installation error
        pause
        exit /b 1
    )
    echo [OK] pywebview установлен / installed
)

:: Run
echo [*] Запуск / Starting...
%PY% "%~dp0src\vs_animator_app.py"
