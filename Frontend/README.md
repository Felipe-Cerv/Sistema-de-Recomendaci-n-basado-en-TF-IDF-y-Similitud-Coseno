# Frontend - Sistema de Recomendación de Libros

Interfaz web simple para el sistema de recomendación de libros.

## Características

- **Búsqueda de libros** con autocompletado
- **Top 20 palabras más relevantes** del libro seleccionado (basado en TF-IDF)
- **Top 10 libros recomendados** con porcentaje de similitud
- **Modal de lectura** con navegación por páginas
- **Atajos de teclado** para navegación rápida
- Diseño responsive y moderno
- Animaciones suaves

## Requisitos

- Backend corriendo en `http://localhost:8000`
- Navegador web moderno (Chrome, Firefox, Edge, Safari)

## Uso

1. **Iniciar el backend** primero:
   ```bash
   cd Backend
   python main.py
   # o
   ./start_server.ps1
   ```

2. **Abrir el frontend**:
   - Simplemente abre `index.html` en tu navegador
   - O usa un servidor local:
     ```bash
     # Python
     python -m http.server 3000
     
     # Node.js (si tienes http-server instalado)
     npx http-server -p 3000
     ```

3. **Buscar un libro**:
   - Escribe el nombre del libro en el campo de búsqueda
   - El autocompletado te mostrará libros disponibles
   - Presiona "Buscar" o Enter
   - ¡Disfruta los resultados!

## Estructura

```
Frontend/
├── index.html      # Estructura HTML
├── styles.css      # Estilos y animaciones
├── app.js          # Lógica de la aplicación
└── README.md       # Este archivo
```

## Ejemplos de nombres de libros

- `Pride_and_Prejudice_by_Jane_Austen`
- `Moby_Dick;_Or,_The_Whale_by_Herman_Melville`
- `Alice's_Adventures_in_Wonderland_by_Lewis_Carroll`
- `Frankenstein;_Or,_The_Modern_Prometheus_by_Mary_Wollstonecraft_Shelley`

## Configuración

Si tu backend corre en un puerto diferente, edita `app.js`:

```javascript
const API_BASE_URL = 'http://localhost:PUERTO/api/v1';
```

## Solución de Problemas

### Error de CORS
Si ves errores de CORS en la consola, asegúrate que el backend tenga CORS habilitado:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Libro no encontrado
Verifica que:
1. El backend esté corriendo
2. Los libros estén analizados (endpoint `/analyze`)
3. El nombre del libro sea exacto (usa el autocompletado)
