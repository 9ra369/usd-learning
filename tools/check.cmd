@echo off
rem Check USD files. With no arguments, checks everything under topics\ and scratch\.
rem   tools\check
rem   tools\check topics\xform\parent_translate.usda
call "%~dp0usd.cmd" python "%~dp0check_usd.py" %*
exit /b %errorlevel%
