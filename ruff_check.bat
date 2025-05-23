@echo off
echo Ejecutando análisis de código con Ruff...
echo.

:: Activa el entorno virtual y ejecuta Ruff
call ..\virtual\Scripts\activate.bat && ruff check . --show-fixes
echo.
echo Análisis de código completado.
pause
