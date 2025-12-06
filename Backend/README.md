# Sistema de Recomendación de Libros - FastAPI Backend

API REST para descarga, procesamiento y análisis de libros usando NLP y Apache Spark.

## Características

- **Descarga de libros** desde Project Gutenberg
- **Limpieza de texto** con procesamiento NLP (NLTK)
- **Análisis TF-IDF** distribuido con Apache Spark
- **Sistema de recomendaciones** basado en similitud coseno
- **Resúmenes automáticos** de libros
- **Lectura de libros** directamente desde la API

## Requisitos

- Python 3.11+
- Java 21+ (para Spark)
- Docker (opcional)

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Copiar archivo de configuración:
```bash
copy .env.example .env
```

## Ejecución

```bash
uvicorn main:app --reload
```

La API estará disponible en: `http://127.0.0.1:8000`

Documentación interactiva: `http://127.0.0.1:8000/docs`

## Endpoints Disponibles

### Books (`/api/v1/books`)

#### 1. Descargar libros
```http
POST /api/v1/books/download
Content-Type: application/json

{
  "n_books": 10
}
```

#### 2. Limpiar libros
```http
POST /api/v1/books/clean
Content-Type: application/json

{
  "clean_all": true
}
```

#### 3. Analizar libros (TF-IDF)
```http
POST /api/v1/books/analyze
```

#### 4. Listar libros disponibles
```http
GET /api/v1/books/books
```

#### 5. Obtener resumen de un libro
```http
POST /api/v1/books/summary
Content-Type: application/json

{
  "book_name": "The_Adventures_of_Sherlock_Holmes.txt",
  "top_words": 20
}
```

#### 6. Obtener recomendaciones
```http
POST /api/v1/books/recommend
Content-Type: application/json

{
  "book_name": "The_Adventures_of_Sherlock_Holmes.txt",
  "k": 5
}
```

#### 7. Health check
```http
GET /api/v1/books/health
```

## Flujo de trabajo típico

1. **Descargar libros**: `POST /books/download` con `n_books: 10`
2. **Limpiar textos**: `POST /books/clean` con `clean_all: true`
3. **Analizar con Spark**: `POST /books/analyze`
4. **Ver libros disponibles**: `GET /books/books`
5. **Obtener recomendaciones**: `POST /books/recommend`

#### 8. Leer contenido de un libro
```http
GET /api/v1/books/read/{book_name}
```

## Flujo de trabajo típico

1. **Descargar libros**: `POST /books/download` con `n_books: 10`
2. **Limpiar textos**: `POST /books/clean` con `clean_all: true`
3. **Analizar con Spark**: `POST /books/analyze`
4. **Ver libros disponibles**: `GET /books`
5. **Obtener recomendaciones**: `POST /books/recommend`
6. **Ver palabras relevantes**: `POST /books/summary`
7. **Leer libro completo**: `GET /books/read/{book_name}`

## Estructura del Proyecto

```
Backend/
├── app/
│   ├── api/v1/endpoints/
│   │   └── books.py      # Endpoints de libros
│   ├── core/
│   │   └── config.py     # Configuración
│   ├── schemas/
│   │   └── book.py       # Modelos Pydantic
│   └── services/
│       ├── book_download.py  # Servicio de descarga
│       ├── book_clean.py     # Servicio de limpieza
│       └── book_analysis.py  # Servicio de análisis
├── data/                 # Datos generados
│   ├── raw_books/       # Libros descargados
│   ├── clean_books/     # Libros procesados
│   └── nltk_data/       # Datos de NLTK
├── Dockerfile           # Contenedor Docker
├── main.py             # Punto de entrada
└── requirements.txt    # Dependencias
```

## Tecnologías

- **FastAPI**: Framework web moderno
- **Apache Spark**: Procesamiento distribuido
- **NLTK**: Procesamiento de lenguaje natural
- **BeautifulSoup**: Web scraping
- **Pydantic**: Validación de datos
- **Docker**: Containerización

## Docker

```bash
# Construir imagen
docker build -t books-backend .

# Ejecutar contenedor
docker run -p 8000:8000 -v ./data:/app/data books-backend
```

O usar docker-compose desde la raíz del proyecto:

```bash
docker-compose up -d
```

## Notas

- El análisis inicial puede tardar varios minutos
- Spark mantendrá los datos en memoria para consultas rápidas
- No requiere base de datos ni autenticación
- Todos los datos se almacenan localmente en archivos
- Los libros se descargan de Project Gutenberg
