from pydantic import BaseModel, Field
from typing import Optional, List

class BookDownloadRequest(BaseModel):
    """Request para descargar libros de Gutenberg"""
    n_books: int = Field(default=10, ge=1, le=100, description="Número de libros a descargar (1-100)")
    
class BookDownloadResponse(BaseModel):
    """Response de descarga de libros"""
    downloaded: int
    failed: int
    message: str

class BookCleanRequest(BaseModel):
    """Request para limpiar libros"""
    book_name: Optional[str] = None
    clean_all: bool = False
    
class BookCleanResponse(BaseModel):
    """Response de limpieza"""
    cleaned_books: int
    message: str

class BookAnalysisResponse(BaseModel):
    """Response del análisis TF-IDF"""
    total_books: int
    message: str
    status: str

class BookSummaryRequest(BaseModel):
    """Request para obtener resumen de un libro"""
    book_name: str
    top_words: int = Field(default=20, ge=5, le=50, description="Número de palabras principales")
    
class BookSummaryResponse(BaseModel):
    """Response con resumen del libro"""
    book_name: str
    summary: str
    top_words: List[tuple]

class BookRecommendationRequest(BaseModel):
    """Request para obtener recomendaciones"""
    book_name: str
    k: int = Field(default=5, ge=1, le=20, description="Número de recomendaciones")
    
class BookRecommendationResponse(BaseModel):
    """Response con recomendaciones"""
    book_name: str
    recommendations: List[dict]

class SimilarityMatrixResponse(BaseModel):
    """Response con matriz de similitud"""
    matrix_size: tuple
    book_names: List[str]
    message: str
