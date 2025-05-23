@echo off
echo Formateando código con Ruff...
echo.

:: Activa el entorno virtual y ejecuta Ruff para formatear el código
call ..\virtual\Scripts\activate.bat && ruff format .
echo.
echo Formateo de código completado.
pause
