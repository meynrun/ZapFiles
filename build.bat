@echo off
title Building...

:: Запрашиваем версию у пользователя
set /p version="Enter version: "

:: Проверка наличия Nuitka
where nuitka >nul 2>nul
if %errorlevel% neq 0 (
    echo Nuitka is not installed. Please install it first.
    exit /b 1
)

:: Копирование папки с локализацией в папку с билдом
set build_dir=.\dist
set localization_dir=.\lang

mkdir .\dist\lang

if exist "%build_dir%" (
    xcopy "%localization_dir%" "%build_dir%\lang" /E /I /Y
    if %errorlevel% neq 0 (
        echo Failed to copy localization files!
        exit /b 1
    ) else (
        echo Localization files copied successfully!
    )
)

:: Запуск Nuitka
nuitka .\main.py --follow-imports --output-dir=dist --jobs=4 --show-progress --windows-icon-from-ico="./assets/ZapFiles-icon.ico" --windows-product-name="ZapFiles" --windows-company-name="MeynDev" --windows-file-version="%version%" --windows-product-version="%version%"

:: Проверка успешности компиляции
if %errorlevel% neq 0 (
    echo Compilation failed!
    exit /b 1
) else (
    echo Compilation successful!
)

exit
