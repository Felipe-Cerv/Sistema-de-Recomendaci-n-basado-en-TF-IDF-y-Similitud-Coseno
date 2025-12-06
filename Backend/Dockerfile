# Imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para PySpark y Java
RUN apt-get update && apt-get install -y \
    openjdk-21-jre-headless \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Detectar y configurar JAVA_HOME automáticamente para cualquier arquitectura (arm64/amd64)
RUN ARCH=$(dpkg --print-architecture) && \
    JAVA_HOME_PATH="/usr/lib/jvm/java-21-openjdk-${ARCH}" && \
    echo "Arquitectura detectada: ${ARCH}" && \
    echo "JAVA_HOME: ${JAVA_HOME_PATH}" && \
    ln -sf "${JAVA_HOME_PATH}" /usr/lib/jvm/default-java

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Copiar archivos de requerimientos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorios necesarios para datos
RUN mkdir -p /app/data/raw_books /app/data/clean_books /app/data/nltk_data

# Descargar datos de NLTK necesarios
RUN python -c "import nltk; nltk.download('punkt', download_dir='/app/data/nltk_data'); nltk.download('stopwords', download_dir='/app/data/nltk_data')"

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
