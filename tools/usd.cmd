@echo off
rem Run a command with the USD environment loaded.
rem   tools\usd usdcat topics\xform\parent_translate.usda
rem   tools\usd python
rem Override the USD install location with the USD_ROOT env var.
rem (Keep this file ASCII-only: cmd.exe may misparse UTF-8 text.)
setlocal
if not defined USD_ROOT set "USD_ROOT=D:\Dev\usd_root"
if not exist "%USD_ROOT%\scripts\set_usd_env.bat" (
    echo [usd] USD not found: %USD_ROOT% 1>&2
    exit /b 1
)
call "%USD_ROOT%\scripts\set_usd_env.bat"
if "%~1"=="" (
    echo usage: tools\usd ^<command^> [args...]
    exit /b 1
)
%*
exit /b %errorlevel%
