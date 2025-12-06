@echo off
REM Script de inicio para el servidor FastAPI (Windows)

REM Intentar detectar JAVA_HOME automaticamente
if "%JAVA_HOME%"=="" (
    if exist "C:\Program Files\Microsoft\jdk-21.0.9.10-hotspot" (
        set JAVA_HOME=C:\Program Files\Microsoft\jdk-21.0.9.10-hotspot
    ) else if exist "C:\Program Files\Java\jdk-21" (
        set JAVA_HOME=C:\Program Files\Java\jdk-21
    ) else if exist "C:\Program Files\OpenJDK\jdk-21" (
        set JAVA_HOME=C:\Program Files\OpenJDK\jdk-21
    ) else if exist "C:\Program Files\Eclipse Adoptium\jdk-21" (
        set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21
    )
)

if defined JAVA_HOME (
    set PATH=%JAVA_HOME%\bin;%PATH%
    echo JAVA_HOME configurado: %JAVA_HOME%
    java -version
) else (
    echo ADVERTENCIA: No se encontro Java 21. PySpark puede no funcionar correctamente.
    echo Por favor instala Java 21 desde: https://adoptium.net/
)

echo Iniciando servidor FastAPI...
uvicorn main:app --reload
