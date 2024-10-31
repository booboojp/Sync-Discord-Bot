@echo off
setlocal

REM Load config file
set "config_file=src\settings\config.json"
for /f "tokens=2 delims=:," %%A in ('findstr /i "token" "%config_file%"') do set "token=%%~A"
for /f "tokens=2 delims=:," %%A in ('findstr /i "version" "%config_file%"') do set "version=%%~A"
for /f "tokens=2 delims=:," %%A in ('findstr /i "main_server_id" "%config_file%"') do set "main_server_id=%%~A"
for /f "tokens=2 delims=:," %%A in ('findstr /i "sync_server_id" "%config_file%"') do set "sync_server_id=%%~A"

REM Check if all required fields are present
if "%token%"=="" (
    echo Missing required config field: token
    exit /b 1
)
if "%version%"=="" (
    echo Missing required config field: version
    exit /b 1
)
if "%main_server_id%"=="" (
    echo Missing required config field: main_server_id
    exit /b 1
)
if "%sync_server_id%"=="" (
    echo Missing required config field: sync_server_id
    exit /b 1
)

REM Clear terminal
cls

REM Start the bot
python src\bot.py
endlocal