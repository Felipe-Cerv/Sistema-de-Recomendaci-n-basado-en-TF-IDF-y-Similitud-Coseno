// Configuración de la API
// Usar variable de entorno o localhost por defecto
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000/api/v1' 
    : 'http://localhost:8000/api/v1';

// Elementos del DOM
const bookInput = document.getElementById('bookInput');
const searchBtn = document.getElementById('searchBtn');
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const results = document.getElementById('results');
const topWords = document.getElementById('topWords');
const recommendations = document.getElementById('recommendations');
const booksList = document.getElementById('booksList');
const toggleLibrary = document.getElementById('toggleLibrary');
const libraryList = document.getElementById('libraryList');
const libraryBooks = document.getElementById('libraryBooks');
const librarySearch = document.getElementById('librarySearch');

let allBooks = [];
let isLibraryOpen = false;

// Cargar lista de libros disponibles al iniciar
async function loadAvailableBooks() {
    try {
        const response = await fetch(`${API_BASE_URL}/books`);
        if (!response.ok) throw new Error('No se pudo cargar la lista de libros');
        
        allBooks = await response.json();
        
        // Llenar el datalist para autocompletado
        allBooks.forEach(book => {
            const option = document.createElement('option');
            option.value = book;
            booksList.appendChild(option);
        });
        
        // Renderizar biblioteca
        renderLibrary(allBooks);
    } catch (err) {
        console.error('Error cargando libros:', err);
    }
}

// Renderizar biblioteca de libros
function renderLibrary(books) {
    libraryBooks.innerHTML = '';
    
    if (books.length === 0) {
        libraryBooks.innerHTML = '<p style="text-align: center; color: #6e6e73; padding: 20px;">No se encontraron libros</p>';
        return;
    }
    
    books.forEach(book => {
        const bookItem = document.createElement('div');
        bookItem.className = 'library-book-item';
        
        const bookTitle = book.replace(/_/g, ' ').replace('.txt', '');
        bookItem.textContent = bookTitle;
        bookItem.title = 'Click para buscar este libro';
        
        bookItem.addEventListener('click', () => {
            // Llenar el input y hacer búsqueda
            bookInput.value = book;
            searchBook();
            
            // Cerrar biblioteca
            toggleLibraryView();
            
            // Scroll al top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        
        libraryBooks.appendChild(bookItem);
    });
}

// Toggle vista de biblioteca
function toggleLibraryView() {
    isLibraryOpen = !isLibraryOpen;
    libraryList.classList.toggle('hidden');
    toggleLibrary.innerHTML = isLibraryOpen 
        ? '<span></span> Ocultar Biblioteca' 
        : '<span></span> Ver Biblioteca Completa';
}

// Buscar en biblioteca
function searchLibrary(query) {
    const filtered = allBooks.filter(book => 
        book.toLowerCase().includes(query.toLowerCase())
    );
    renderLibrary(filtered);
}

// Mostrar error
function showError(message) {
    error.textContent = message;
    error.classList.remove('hidden');
    results.classList.add('hidden');
    loading.classList.add('hidden');
}

// Ocultar error
function hideError() {
    error.classList.add('hidden');
}

// Mostrar loading
function showLoading() {
    loading.classList.remove('hidden');
    results.classList.add('hidden');
    hideError();
}

// Ocultar loading
function hideLoading() {
    loading.classList.add('hidden');
}

// Obtener palabras relevantes
async function getTopWords(bookName) {
    const response = await fetch(`${API_BASE_URL}/books/summary`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            book_name: bookName,
            top_words: 20
        })
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error obteniendo palabras relevantes');
    }
    
    return await response.json();
}

// Obtener recomendaciones
async function getRecommendations(bookName) {
    const response = await fetch(`${API_BASE_URL}/books/recommend`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            book_name: bookName,
            k: 10
        })
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error obteniendo recomendaciones');
    }
    
    return await response.json();
}

// Renderizar palabras relevantes
function renderTopWords(words) {
    topWords.innerHTML = '';
    
    words.forEach((wordData, index) => {
        const wordTag = document.createElement('div');
        wordTag.className = 'word-tag';
        wordTag.style.animationDelay = `${index * 0.05}s`;
        
        // wordData es un array [palabra, score]
        const word = wordData[0];
        const score = wordData[1];
        
        wordTag.innerHTML = `
            <span class="word">${word}</span>
            <span class="score">${score.toFixed(2)}</span>
        `;
        
        topWords.appendChild(wordTag);
    });
}

// Renderizar recomendaciones
function renderRecommendations(recs) {
    recommendations.innerHTML = '';
    
    recs.forEach((rec, index) => {
        const card = document.createElement('div');
        card.className = 'recommendation-card';
        card.style.animationDelay = `${index * 0.1}s`;
        card.style.cursor = 'pointer';
        card.title = 'Click para leer el libro';
        
        const bookTitle = rec.book_name.replace(/_/g, ' ').replace('.txt', '');
        const similarityPercent = (rec.similarity * 100).toFixed(2);
        
        card.innerHTML = `
            <div class="recommendation-rank">#${index + 1}</div>
            <div class="recommendation-info">
                <div class="recommendation-title">${bookTitle}</div>
                <div class="recommendation-similarity">
                    <div class="similarity-bar">
                        <div class="similarity-fill" style="width: ${similarityPercent}%"></div>
                    </div>
                    <div class="similarity-value">${similarityPercent}%</div>
                </div>
            </div>
            <div class="read-icon">[Leer]</div>
        `;
        
        // Agregar evento click para abrir el libro en el modal
        card.addEventListener('click', () => {
            openBookModal(rec.book_name);
        });
        
        recommendations.appendChild(card);
    });
}

// Buscar libro
async function searchBook() {
    const bookName = bookInput.value.trim();
    
    if (!bookName) {
        showError('Por favor, ingresa el nombre de un libro');
        return;
    }
    
    showLoading();
    
    try {
        // Obtener ambos resultados en paralelo
        const [summaryData, recommendationsData] = await Promise.all([
            getTopWords(bookName),
            getRecommendations(bookName)
        ]);
        
        // Renderizar resultados
        renderTopWords(summaryData.top_words);
        renderRecommendations(recommendationsData.recommendations);
        
        // Mostrar resultados
        hideLoading();
        results.classList.remove('hidden');
        
    } catch (err) {
        showError(err.message);
    }
}

// Variables del modal
const bookModal = document.getElementById('bookModal');
const closeModalBtn = document.getElementById('closeModal');
const modalBookTitle = document.getElementById('modalBookTitle');
const bookContent = document.getElementById('bookContent');
const pageInfo = document.getElementById('pageInfo');
const firstPageBtn = document.getElementById('firstPage');
const prevPageBtn = document.getElementById('prevPage');
const nextPageBtn = document.getElementById('nextPage');
const lastPageBtn = document.getElementById('lastPage');
const pageInput = document.getElementById('pageInput');
const linesPerPageSelect = document.getElementById('linesPerPage');

let currentBookContent = '';
let currentBookName = '';
let currentPage = 1;
let totalPages = 1;
let linesPerPage = 30;
let bookLines = [];

// Abrir modal y cargar libro
async function openBookModal(bookName) {
    try {
        bookModal.classList.remove('hidden');
        bookModal.classList.add('show');
        bookContent.innerHTML = '<p style="text-align: center;">Cargando libro...</p>';
        
        currentBookName = bookName;
        const bookTitle = bookName.replace(/_/g, ' ').replace('.txt', '');
        modalBookTitle.textContent = bookTitle;
        
        // Cargar contenido del libro
        const response = await fetch(`${API_BASE_URL}/books/read/${encodeURIComponent(bookName)}`);
        if (!response.ok) throw new Error('No se pudo cargar el libro');
        
        currentBookContent = await response.text();
        bookLines = currentBookContent.split('\n');
        
        // Calcular total de páginas
        totalPages = Math.ceil(bookLines.length / linesPerPage);
        currentPage = 1;
        
        // Mostrar primera página
        displayPage(currentPage);
        
    } catch (err) {
        bookContent.innerHTML = `<p style="color: red; text-align: center;">Error: ${err.message}</p>`;
    }
}

// Mostrar página específica
function displayPage(pageNum) {
    if (pageNum < 1) pageNum = 1;
    if (pageNum > totalPages) pageNum = totalPages;
    
    currentPage = pageNum;
    
    const startLine = (currentPage - 1) * linesPerPage;
    const endLine = Math.min(startLine + linesPerPage, bookLines.length);
    
    const pageContent = bookLines.slice(startLine, endLine).join('\n');
    bookContent.textContent = pageContent;
    
    // Actualizar info de página
    pageInfo.textContent = `Página ${currentPage} de ${totalPages}`;
    pageInput.value = currentPage;
    pageInput.max = totalPages;
    
    // Actualizar botones
    firstPageBtn.disabled = currentPage === 1;
    prevPageBtn.disabled = currentPage === 1;
    nextPageBtn.disabled = currentPage === totalPages;
    lastPageBtn.disabled = currentPage === totalPages;
    
    // Scroll al inicio del contenido
    bookContent.parentElement.scrollTop = 0;
}

// Cerrar modal
function closeBookModal() {
    bookModal.classList.remove('show');
    bookModal.classList.add('hidden');
}

// Event listeners del modal
closeModalBtn.addEventListener('click', closeBookModal);

bookModal.addEventListener('click', (e) => {
    if (e.target === bookModal) {
        closeBookModal();
    }
});

firstPageBtn.addEventListener('click', () => displayPage(1));
prevPageBtn.addEventListener('click', () => displayPage(currentPage - 1));
nextPageBtn.addEventListener('click', () => displayPage(currentPage + 1));
lastPageBtn.addEventListener('click', () => displayPage(totalPages));

pageInput.addEventListener('change', (e) => {
    const page = parseInt(e.target.value);
    if (!isNaN(page)) {
        displayPage(page);
    }
});

linesPerPageSelect.addEventListener('change', (e) => {
    linesPerPage = parseInt(e.target.value);
    totalPages = Math.ceil(bookLines.length / linesPerPage);
    displayPage(1); // Volver a primera página con nuevo tamaño
});

// Navegación con teclado
document.addEventListener('keydown', (e) => {
    if (!bookModal.classList.contains('show')) return;
    
    if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        displayPage(currentPage - 1);
    } else if (e.key === 'ArrowRight' || e.key === 'PageDown') {
        e.preventDefault();
        displayPage(currentPage + 1);
    } else if (e.key === 'Home') {
        e.preventDefault();
        displayPage(1);
    } else if (e.key === 'End') {
        e.preventDefault();
        displayPage(totalPages);
    } else if (e.key === 'Escape') {
        closeBookModal();
    }
});

// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');

// Cargar tema guardado
const savedTheme = localStorage.getItem('theme') || 'light';
if (savedTheme === 'dark') {
    document.body.classList.add('dark-mode');
    themeIcon.textContent = '☀️';
}

themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    themeIcon.textContent = isDark ? '☀️' : '🌙';
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
});

// Event listeners
searchBtn.addEventListener('click', searchBook);

bookInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        searchBook();
    }
});

toggleLibrary.addEventListener('click', toggleLibraryView);

librarySearch.addEventListener('input', (e) => {
    searchLibrary(e.target.value);
});

// Cargar libros disponibles al iniciar
loadAvailableBooks();
