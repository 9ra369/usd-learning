@echo off
rem Open a file in usdview.
rem   tools\view topics\purpose\box_proxy.usda
call "%~dp0usd.cmd" usdview %*
exit /b %errorlevel%
