#!/bin/bash
# Script de inicio para el servidor FastAPI (Mac/Linux)

# Detectar JAVA_HOME automáticamente si no está configurado
if [ -z "$JAVA_HOME" ]; then
    # Intentar encontrar Java en Mac
    if [ -x /usr/libexec/java_home ]; then
        export JAVA_HOME=$(/usr/libexec/java_home -v 21 2>/dev/null || /usr/libexec/java_home 2>/dev/null)
    fi
    
    # Si aún no se encuentra, buscar en rutas comunes de Linux
    if [ -z "$JAVA_HOME" ] && [ -d /usr/lib/jvm/java-21-openjdk-amd64 ]; then
        export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
    elif [ -z "$JAVA_HOME" ] && [ -d /usr/lib/jvm/java-21-openjdk ]; then
        export JAVA_HOME=/usr/lib/jvm/java-21-openjdk
    fi
fi

if [ -n "$JAVA_HOME" ]; then
    export PATH="$JAVA_HOME/bin:$PATH"
    echo "✓ JAVA_HOME configurado: $JAVA_HOME"
    java -version
else
    echo "⚠ ADVERTENCIA: No se encontró Java 21. PySpark puede no funcionar correctamente."
    echo "Por favor instala Java 21:"
    echo "  - Mac: brew install openjdk@21"
    echo "  - Linux: sudo apt-get install openjdk-21-jre-headless"
fi

echo "Iniciando servidor FastAPI..."
uvicorn main:app --reload
