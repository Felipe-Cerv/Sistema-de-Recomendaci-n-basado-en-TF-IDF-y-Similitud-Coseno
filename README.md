# Sistema de Recomendación de Libros

Sistema completo de recomendación de libros basado en TF-IDF y Similitud Coseno, con análisis distribuido usando Apache Spark.

## Arquitectura

- **Backend**: FastAPI + PySpark para procesamiento distribuido
- **Frontend**: HTML/CSS/JavaScript con interfaz moderna
- **Docker**: Contenedores para fácil despliegue

## Características

- Descarga automática de libros desde Project Gutenberg
- Limpieza y preprocesamiento de texto con NLTK
- Análisis TF-IDF distribuido con Apache Spark
- Recomendaciones basadas en similitud coseno
- Interfaz web interactiva con:
  - Búsqueda con autocompletado
  - Top 20 palabras más relevantes
  - Top 10 libros recomendados
  - Lector integrado con navegación por páginas
  - Atajos de teclado para navegación rápida

## Requisitos

- Docker y Docker Compose instalados
- 4GB de RAM mínimo (recomendado 8GB para Spark)
- Puertos 80 y 8000 disponibles

## Inicio Rápido con Docker

### 1. Clonar o ubicarse en el directorio del proyecto

```bash
cd ProyectoFinal
```

### 2. Construir y ejecutar los contenedores

```bash
docker-compose up -d
```

Esto iniciará:
- Backend en `http://localhost:8000`
- Frontend en `http://localhost:80`

### 3. Verificar que los servicios estén corriendo

```bash
docker-compose ps
```

### 4. Ver los logs

```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend
```

### 5. Acceder a la aplicación

Abre tu navegador en `http://localhost`

## Uso de la Aplicación

### Primera vez

1. **Analizar libros** (si no se han analizado):
   ```bash
   curl -X POST http://localhost:8000/api/v1/books/analyze
   ```
   
   Este proceso puede tardar varios minutos la primera vez.

2. **Verificar libros disponibles**:
   ```bash
   curl http://localhost:8000/api/v1/books
   ```

### Interfaz Web

1. Abre `http://localhost` en tu navegador
2. Escribe el nombre de un libro (usa el autocompletado)
3. Presiona "Buscar"
4. Verás:
   - Las 20 palabras más relevantes del libro
   - Los 10 libros más similares recomendados
5. Haz click en cualquier recomendación para leer el libro completo

### Lector de Libros

- **Navegación con botones**: Primera, Anterior, Siguiente, Última
- **Saltar a página**: Escribe el número y presiona Enter
- **Líneas por página**: Selecciona 20, 30, 50 o 100 líneas
- **Atajos de teclado**:
  - `←` o `PageUp`: Página anterior
  - `→` o `PageDown`: Página siguiente
  - `Home`: Primera página
  - `End`: Última página
  - `Esc`: Cerrar lector

## API Endpoints

### Libros

- `GET /api/v1/books` - Lista libros disponibles
- `POST /api/v1/books/download` - Descarga libros de Gutenberg
- `POST /api/v1/books/clean` - Limpia libros descargados
- `POST /api/v1/books/analyze` - Analiza libros con TF-IDF
- `POST /api/v1/books/summary` - Obtiene palabras relevantes
- `POST /api/v1/books/recommend` - Obtiene recomendaciones
- `GET /api/v1/books/read/{book_name}` - Lee contenido del libro
- `GET /api/v1/books/health` - Estado del servicio

### Documentación Interactiva

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Comandos Docker Útiles

### Detener los servicios

```bash
docker-compose down
```

### Detener y eliminar volúmenes (reinicio completo)

```bash
docker-compose down -v
```

### Reconstruir las imágenes

```bash
docker-compose build --no-cache
docker-compose up -d
```

### Acceder al contenedor backend

```bash
docker exec -it books-backend bash
```

### Acceder al contenedor frontend

```bash
docker exec -it books-frontend sh
```

### Ver uso de recursos

```bash
docker stats
```

## Desarrollo Local (sin Docker)

### Backend

```bash
cd Backend
pip install -r requirements.txt
python main.py
# o
uvicorn main:app --reload
```

### Frontend

```bash
cd Frontend
# Opción 1: Abrir index.html directamente en el navegador
# Opción 2: Usar servidor local
python -m http.server 3000
```

## Estructura del Proyecto

```
ProyectoFinal/
├── Backend/
│   ├── app/
│   │   ├── api/          # Endpoints REST
│   │   ├── core/         # Configuración
│   │   ├── models/       # Modelos de datos
│   │   ├── schemas/      # Schemas Pydantic
│   │   └── services/     # Lógica de negocio
│   ├── data/
│   │   ├── raw_books/    # Libros originales
│   │   ├── clean_books/  # Libros procesados
│   │   └── nltk_data/    # Datos de NLTK
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
├── Frontend/
│   ├── index.html        # Estructura HTML
│   ├── styles.css        # Estilos y animaciones
│   ├── app.js           # Lógica de la aplicación
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Variables de Entorno

Backend (`.env`):
```env
BOOKS_RAW_PATH=./data/raw_books
BOOKS_CLEAN_PATH=./data/clean_books
NLTK_DATA_DIR=./data/nltk_data
```

## Solución de Problemas

### El backend no inicia

- Verificar logs: `docker-compose logs backend`
- Asegurar que Java esté instalado en el contenedor (necesario para Spark)
- Verificar que los puertos no estén en uso

### El frontend no se conecta al backend

- Verificar que el backend esté corriendo: `curl http://localhost:8000/api/v1/books/health`
- Revisar configuración de CORS en el backend
- Verificar red de Docker: `docker network inspect proyectofinal_books-network`

### Análisis de libros falla

- El análisis requiere tiempo y recursos
- Verificar logs de Spark en el contenedor backend
- Asegurar suficiente RAM disponible (mínimo 4GB)

### Los libros no se leen en el modal

- Verificar que los archivos existen en `Backend/data/raw_books/`
- Verificar permisos de archivos
- Revisar logs del backend para errores

## Tecnologías Utilizadas

- **Backend**: FastAPI, PySpark, NLTK, Uvicorn
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Análisis**: Apache Spark, TF-IDF, Similitud Coseno
- **Datos**: Project Gutenberg
- **Containerización**: Docker, Docker Compose
- **Web Server**: Nginx (Frontend)

## Licencia

Este proyecto es para fines educativos.

## Autores

Proyecto Final - Sistemas Distribuidos
