import os
import re
from pathlib import Path
from typing import Optional
import nltk
from nltk.corpus import stopwords
from app.core.config import settings

class BookCleanService:
    """Servicio para limpiar y procesar texto de libros"""
    
    def __init__(self):
        self.books_raw_path = Path(settings.BOOKS_RAW_PATH)
        self.books_clean_path = Path(settings.BOOKS_CLEAN_PATH)
        self.books_clean_path.mkdir(parents=True, exist_ok=True)
        
        # Configurar NLTK
        self._setup_nltk()
    
    def _setup_nltk(self):
        """Configura y descarga recursos de NLTK si es necesario"""
        nltk_data_dir = Path(settings.NLTK_DATA_DIR)
        nltk_data_dir.mkdir(parents=True, exist_ok=True)
        nltk.data.path.append(str(nltk_data_dir.resolve()))
        
        required_packages = ["punkt", "stopwords"]
        for pkg in required_packages:
            try:
                if pkg == "punkt":
                    nltk.data.find(f'tokenizers/{pkg}')
                elif pkg == "stopwords":
                    nltk.data.find(f'corpora/{pkg}')
            except LookupError:
                try:
                    nltk.download(pkg, download_dir=str(nltk_data_dir.resolve()), quiet=True)
                except Exception as e:
                    print(f"Error descargando {pkg}: {e}")
        
        # Cargar stopwords
        try:
            self.stopwords = set(stopwords.words("english"))
        except:
            self.stopwords = set()
    
    def limpiar_texto(self, texto: str) -> str:
        """Normaliza texto: minúsculas, elimina no-alfabéticos y stopwords."""
        texto = texto.lower()
        palabras = re.findall(r"[a-záéíóúüñ]+", texto)
        palabras = [p for p in palabras if p not in self.stopwords and len(p) > 1]
        return " ".join(palabras)
    
    def clean_book(self, book_name: str) -> bool:
        """Limpia un libro específico"""
        raw_path = self.books_raw_path / book_name
        clean_path = self.books_clean_path / book_name
        
        if not raw_path.exists():
            return False
        
        try:
            with open(raw_path, encoding="utf-8") as f:
                texto = f.read()
        except UnicodeDecodeError:
            with open(raw_path, "rb") as f:
                texto = f.read().decode("utf-8", errors="ignore")
        except Exception:
            return False
        
        limpio = self.limpiar_texto(texto)
        
        with open(clean_path, "w", encoding="utf-8") as f:
            f.write(limpio)
        
        return True
    
    def clean_all_books(self) -> int:
        """Limpia todos los libros en la carpeta raw"""
        books_raw = [a for a in os.listdir(str(self.books_raw_path)) if a.endswith(".txt")]
        
        cleaned_count = 0
        for archivo in books_raw:
            if self.clean_book(archivo):
                cleaned_count += 1
        
        return cleaned_count
