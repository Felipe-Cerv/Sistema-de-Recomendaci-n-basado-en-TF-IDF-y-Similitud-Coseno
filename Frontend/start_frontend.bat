@echo off
echo ========================================
echo   Sistema de Recomendacion de Libros
echo   Iniciando Frontend...
echo ========================================
echo.

REM Verificar si Python esta disponible
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python o abre index.html directamente en tu navegador
    pause
    exit /b 1
)

echo Iniciando servidor local en http://localhost:3000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.
echo NOTA: Asegurate de que el backend este corriendo en http://localhost:8000
echo.

REM Iniciar servidor HTTP simple con Python
cd /d "%~dp0"
python -m http.server 3000

pause
