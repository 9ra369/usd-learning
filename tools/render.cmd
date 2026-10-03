@echo off
rem Render a file to renders\<name>.png with usdrecord.
rem   tools\render topics\purpose\box_proxy.usda
rem   tools\render topics\purpose\box_proxy.usda --purposes render
rem Arguments after the file are passed through to usdrecord.
setlocal
rem Save our own dir first: "shift" also shifts %0, which breaks %~dp0.
set "HERE=%~dp0"
if "%~1"=="" (
    echo usage: tools\render ^<file.usda^> [usdrecord options...]
    exit /b 1
)
set "SRC=%~1"
set "OUT=%HERE%..\renders\%~n1.png"
if not exist "%HERE%..\renders" mkdir "%HERE%..\renders"
shift
set "OPTS="
:collect
if "%~1"=="" goto run
set "OPTS=%OPTS% %1"
shift
goto collect
:run
call "%HERE%usd.cmd" usdrecord --imageWidth 800 %OPTS% "%SRC%" "%OUT%"
if errorlevel 1 exit /b %errorlevel%
for %%F in ("%OUT%") do echo wrote: %%~fF
