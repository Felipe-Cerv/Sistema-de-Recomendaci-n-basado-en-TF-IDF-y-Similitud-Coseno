# Script de inicio para el servidor FastAPI con Java configurado
$env:JAVA_HOME = "C:\Program Files\Microsoft\jdk-21.0.9.10-hotspot"
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"

Write-Host "JAVA_HOME configurado: $env:JAVA_HOME" -ForegroundColor Green
Write-Host "Iniciando servidor FastAPI..." -ForegroundColor Cyan

uvicorn main:app --reload
