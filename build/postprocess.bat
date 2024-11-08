@echo off
title Post-processing...

:: Путь к папке с билдом
set build_dir=.\dist
set localization_dir=.\lang

:: Проверка и удаление существующей папки lang в директории dist
if exist "%build_dir%\lang" (
    rd /s /q "%build_dir%\lang"
)

mkdir "%build_dir%\lang"

:: Копирование папки с локализацией в папку с билдом
if exist "%build_dir%" (
    xcopy "%localization_dir%" "%build_dir%\lang" /E /I /Y
    if %errorlevel% neq 0 (
        echo Failed to copy localization files!
        exit /b 1
    ) else (
        echo Localization files copied successfully!
    )
)

:: Удаление временных файлов и папок
if exist "%build_dir%\main.dist" (
    rd /s /q "%build_dir%\main.dist"
)

if exist "%build_dir%\main.build" (
    rd /s /q "%build_dir%\main.build"
)

if exist "%build_dir%\main.onefile-build" (
    rd /s /q "%build_dir%\main.onefile-build"
)

exit
