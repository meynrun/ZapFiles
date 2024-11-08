@echo off
title Compiling...

:: Запрашиваем версию у пользователя
set /p version="Enter version: "

:: Проверка наличия Nuitka
where nuitka >nul 2>nul
if %errorlevel% neq 0 (
    echo Nuitka is not installed. Please install it first.
    exit /b 1
)

:: Запуск Nuitka
nuitka .\main.py --onefile --standalone --no-pyi-file --output-dir=dist --jobs=4 --show-progress --windows-icon-from-ico="./assets/ZapFiles-icon.ico" --windows-product-name="ZapFiles" --windows-company-name="MeynDev" --windows-file-version="%version%" --windows-product-version="%version%"

:: Проверка успешности компиляции
if %errorlevel% neq 0 (
    echo Compilation failed!
    exit /b 1
) else (
    echo Compilation successful!
)

exit
