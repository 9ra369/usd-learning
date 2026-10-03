@echo off
rem Create a new topic folder from templates\.
rem   tools\new materials            -> topics\materials\README.md + sample.usda
rem   tools\new materials preview    -> topics\materials\README.md + preview.usda
setlocal
set "HERE=%~dp0"
if "%~1"=="" (
    echo usage: tools\new ^<topic^> [sample-name]
    exit /b 1
)
set "DIR=%HERE%..\topics\%~1"
set "SAMPLE=%~2"
if "%SAMPLE%"=="" set "SAMPLE=sample"
if exist "%DIR%\README.md" (
    echo already exists: topics\%~1\README.md 1>&2
    exit /b 1
)
mkdir "%DIR%" 2>nul
copy /y "%HERE%..\templates\topic.md" "%DIR%\README.md" >nul
if not exist "%DIR%\%SAMPLE%.usda" copy /y "%HERE%..\templates\sample.usda" "%DIR%\%SAMPLE%.usda" >nul
echo created: topics\%~1\README.md
echo created: topics\%~1\%SAMPLE%.usda
echo next: add the topic to topics\README.md
