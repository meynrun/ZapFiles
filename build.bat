@echo off
title Building All...

:: Выполнение компиляции
echo Starting compile.bat...
call build\compile.bat
if %errorlevel% neq 0 (
    echo Compilation script failed! Exiting...
    exit /b 1
)

:: Выполнение постобработки
echo Starting postprocess.bat...
call build\postprocess.bat
if %errorlevel% neq 0 (
    echo Postprocessing script failed! Exiting...
    exit /b 1
)

:: Выполнение компиляции setup
echo Starting compile_setup.bat...
call build\compile_setup.bat
if %errorlevel% neq 0 (
    echo Compiling setup failed! Exiting...
    exit /b 1
)

echo All steps completed successfully!
exit
