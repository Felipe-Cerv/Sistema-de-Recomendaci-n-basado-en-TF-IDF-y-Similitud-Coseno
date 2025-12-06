import os
import re
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from typing import Tuple, List, Union
from app.core.config import settings

class BookDownloadService:
    """Servicio para descargar libros desde Project Gutenberg"""
    
    def __init__(self):
        self.base_url = "https://www.gutenberg.org"
        self.books_raw_path = Path(settings.BOOKS_RAW_PATH)
        self.books_raw_path.mkdir(parents=True, exist_ok=True)
    
    def get_links(self, n: Union[int, List[int]] = -1) -> Tuple[List[str], List[str]]:
        """Obtiene enlaces y títulos de los libros más populares de Gutenberg."""
        url = f"{self.base_url}/browse/scores/top"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            parser = BeautifulSoup(response.text, "html.parser")
            ordered_list = parser.find("ol")
            
            if not ordered_list:
                return [], []
            
            list_items = ordered_list.find_all("li")
            
            if n != -1:
                indices = list(n) if isinstance(n, (list, range)) else [n]
                list_filtered = [list_items[i - 1] for i in indices if 0 < i <= len(list_items)]
            else:
                list_filtered = list_items
            
            suffix = ".txt.utf-8"
            links, titles = [], []
            
            for li in list_filtered:
                link_tag = li.find("a")
                if link_tag and link_tag.get("href"):
                    links.append(self.base_url + link_tag.get("href") + suffix)
                    title = re.sub(r"\s+", "_", li.get_text())
                    title = re.sub(r"_\(\d+\)$", "", title)
                    title += ".txt"
                    titles.append(title)
            
            return links, titles
            
        except Exception as e:
            print(f"Error en get_links: {e}")
            return [], []
    
    def download_file(self, url: str, name: str) -> bool:
        """Descarga un archivo individual."""
        try:
            file_path = self.books_raw_path / name
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(file_path, mode="wb") as file:
                for chunk in response.iter_content(chunk_size=10 * 1024):
                    file.write(chunk)
            return True
        except Exception as e:
            print(f"Error descargando {name}: {e}")
            return False
    
    def download_books(self, n_books: int = 10) -> Tuple[int, int]:
        """Descarga n libros usando threading."""
        links, titles = self.get_links(range(1, n_books + 1))
        
        if not links:
            return 0, 0
        
        results = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(self.download_file, links, titles))
        
        downloaded = sum(results)
        failed = len(results) - downloaded
        
        return downloaded, failed
