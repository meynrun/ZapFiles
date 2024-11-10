@echo off
title Compiling Setup...

set INNO_SETUP_PATH="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
set ISS_FILE=".\setup_script.iss"

echo Compiling setup...
%INNO_SETUP_PATH% %ISS_FILE%

if %errorlevel% neq 0 (
    exit /b 1
) else (
    echo Setup compiled successfully
)