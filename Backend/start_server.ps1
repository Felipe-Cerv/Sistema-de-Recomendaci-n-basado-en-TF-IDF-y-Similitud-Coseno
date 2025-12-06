# Script de inicio para el servidor FastAPI con Java configurado (Windows)

# Intentar detectar JAVA_HOME automáticamente si no está configurado
if (-not $env:JAVA_HOME) {
    # Buscar en rutas comunes de Windows
    $possiblePaths = @(
        "C:\Program Files\Microsoft\jdk-21.0.9.10-hotspot",
        "C:\Program Files\Java\jdk-21",
        "C:\Program Files\OpenJDK\jdk-21",
        "C:\Program Files\Eclipse Adoptium\jdk-21"
    )
    
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            $env:JAVA_HOME = $path
            break
        }
    }
}

if ($env:JAVA_HOME) {
    $env:PATH = "$env:JAVA_HOME\bin;$env:PATH"
    Write-Host "JAVA_HOME configurado: $env:JAVA_HOME" -ForegroundColor Green
    java -version
} else {
    Write-Host "ADVERTENCIA: No se encontro Java 21. PySpark puede no funcionar correctamente." -ForegroundColor Yellow
    Write-Host "Por favor instala Java 21 desde: https://adoptium.net/" -ForegroundColor Yellow
}

Write-Host "Iniciando servidor FastAPI..." -ForegroundColor Cyan
uvicorn main:app --reload
