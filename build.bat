@echo off
title Building All...

:: Выполнение компиляции
call build\compile.bat
if %errorlevel% neq 0 (
    echo Compilation script failed! Exiting...
    exit /b 1
)

:: Выполнение постобработки
call build\postprocess.bat
if %errorlevel% neq 0 (
    echo Postprocessing script failed! Exiting...
    exit /b 1
)

echo All steps completed successfully!
exit
