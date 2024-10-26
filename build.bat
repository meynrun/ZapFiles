@echo off
title Building...

:: Проверка наличия Nuitka
where nuitka >nul 2>nul
if %errorlevel% neq 0 (
    echo Nuitka is not installed. Please install it first.
    exit /b 1
)

:: Запуск Nuitka
nuitka .\main.py --standalone --onefile --output-dir=dist --jobs=4

:: Проверка успешности компиляции
if %errorlevel% neq 0 (
    echo Compilation failed!
    exit /b 1
) else (
    echo Compilation successful!
)

exit
