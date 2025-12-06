Write-Host "========================================"
Write-Host "  Sistema de Recomendacion de Libros"
Write-Host "  Iniciando Frontend..."
Write-Host "========================================"
Write-Host ""

# Verificar si Python esta disponible
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python encontrado: $pythonVersion"
} catch {
    Write-Host "Error: Python no esta instalado o no esta en el PATH" -ForegroundColor Red
    Write-Host "Por favor instala Python o abre index.html directamente en tu navegador" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "Iniciando servidor local en http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""
Write-Host "NOTA: Asegurate de que el backend este corriendo en http://localhost:8000" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio del script
Set-Location -Path $PSScriptRoot

# Iniciar servidor HTTP simple con Python
python -m http.server 3000
