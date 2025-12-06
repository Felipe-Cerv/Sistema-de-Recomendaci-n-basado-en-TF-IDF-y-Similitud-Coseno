from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from typing import List
from app.schemas.book import (
    BookDownloadRequest, 
    BookDownloadResponse,
    BookCleanRequest,
    BookCleanResponse,
    BookAnalysisResponse,
    BookSummaryRequest,
    BookSummaryResponse,
    BookRecommendationRequest,
    BookRecommendationResponse
)
from app.services.book_download import BookDownloadService
from app.services.book_clean import BookCleanService
from app.services.book_analysis import BookAnalysisService
from app.core.config import settings
import os

router = APIRouter()

# Instancias de servicios
download_service = BookDownloadService()
clean_service = BookCleanService()
analysis_service = BookAnalysisService()

@router.post("/download", response_model=BookDownloadResponse)
async def download_books(request: BookDownloadRequest, background_tasks: BackgroundTasks):
    """
    Descarga libros desde Project Gutenberg.
    
    - **n_books**: Número de libros a descargar (1-100)
    """
    try:
        downloaded, failed = download_service.download_books(request.n_books)
        
        return BookDownloadResponse(
            downloaded=downloaded,
            failed=failed,
            message=f"Descargados {downloaded} libros, {failed} fallidos"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en descarga: {str(e)}")

@router.post("/clean", response_model=BookCleanResponse)
async def clean_books(request: BookCleanRequest):
    """
    Limpia y procesa libros descargados.
    
    - **book_name**: Nombre específico del libro a limpiar (opcional)
    - **clean_all**: Si es True, limpia todos los libros
    """
    try:
        if request.clean_all:
            cleaned = clean_service.clean_all_books()
            return BookCleanResponse(
                cleaned_books=cleaned,
                message=f"Se limpiaron {cleaned} libros"
            )
        elif request.book_name:
            success = clean_service.clean_book(request.book_name)
            if success:
                return BookCleanResponse(
                    cleaned_books=1,
                    message=f"Libro '{request.book_name}' limpiado exitosamente"
                )
            else:
                raise HTTPException(status_code=404, detail="Libro no encontrado")
        else:
            raise HTTPException(status_code=400, detail="Debe especificar book_name o clean_all=True")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en limpieza: {str(e)}")

@router.post("/analyze", response_model=BookAnalysisResponse)
async def analyze_books():
    """
    Realiza análisis TF-IDF de todos los libros limpios.
    
    Este proceso puede tardar varios minutos dependiendo del número de libros.
    """
    try:
        success = analysis_service.load_and_analyze()
        
        if not success:
            raise HTTPException(
                status_code=404, 
                detail="No hay libros limpios para analizar. Ejecuta primero /clean"
            )
        
        total_books = len(analysis_service.docs)
        
        return BookAnalysisResponse(
            total_books=total_books,
            message=f"Análisis completado para {total_books} libros",
            status="success"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en análisis: {str(e)}")

@router.get("/", response_model=List[str])
async def list_books():
    """
    Lista todos los libros analizados disponibles para consulta.
    """
    try:
        if not analysis_service.docs:
            analysis_service.load_and_analyze()
        
        books = analysis_service.get_all_books()
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando libros: {str(e)}")

@router.post("/summary", response_model=BookSummaryResponse)
async def get_book_summary(request: BookSummaryRequest):
    """
    Obtiene un resumen del libro basado en las palabras más relevantes (TF-IDF).
    
    - **book_name**: Nombre del libro
    - **top_words**: Número de palabras principales (5-50)
    """
    try:
        if not analysis_service.docs:
            analysis_service.load_and_analyze()
        
        book_path = analysis_service.get_book_path(request.book_name)
        
        if not book_path:
            raise HTTPException(
                status_code=404, 
                detail=f"Libro '{request.book_name}' no encontrado. Usa /books para ver disponibles"
            )
        
        summary = analysis_service.get_summary(book_path, request.top_words)
        top_words = analysis_service.get_top_words(book_path, request.top_words)
        
        return BookSummaryResponse(
            book_name=os.path.basename(book_path),
            summary=summary,
            top_words=top_words
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo resumen: {str(e)}")

@router.post("/recommend", response_model=BookRecommendationResponse)
async def get_recommendations(request: BookRecommendationRequest):
    """
    Obtiene recomendaciones de libros similares basadas en similitud coseno.
    
    - **book_name**: Nombre del libro base
    - **k**: Número de recomendaciones (1-20)
    """
    try:
        if not analysis_service.docs:
            analysis_service.load_and_analyze()
        
        book_path = analysis_service.get_book_path(request.book_name)
        
        if not book_path:
            raise HTTPException(
                status_code=404, 
                detail=f"Libro '{request.book_name}' no encontrado. Usa /books para ver disponibles"
            )
        
        recommendations = analysis_service.get_recommendations(book_path, request.k)
        
        # Formatear recomendaciones
        formatted_recs = [
            {
                "book_name": os.path.basename(doc),
                "similarity": round(sim, 4)
            }
            for doc, sim in recommendations
        ]
        
        return BookRecommendationResponse(
            book_name=os.path.basename(book_path),
            recommendations=formatted_recs
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo recomendaciones: {str(e)}")

@router.get("/read/{book_name:path}")
async def read_book(book_name: str):
    """
    Obtiene el contenido RAW de un libro para leerlo.
    
    - **book_name**: Nombre del libro (con extensión .txt)
    """
    try:
        # Buscar primero en raw_books
        raw_path = os.path.join(settings.BOOKS_RAW_PATH, book_name)
        
        if os.path.exists(raw_path):
            return FileResponse(
                path=raw_path,
                media_type="text/plain; charset=utf-8",
                filename=book_name
            )
        
        # Si no está en raw, buscar en clean_books
        clean_path = os.path.join(settings.BOOKS_CLEAN_PATH, book_name)
        
        if os.path.exists(clean_path):
            return FileResponse(
                path=clean_path,
                media_type="text/plain; charset=utf-8",
                filename=book_name
            )
        
        raise HTTPException(status_code=404, detail=f"Libro '{book_name}' no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error leyendo libro: {str(e)}")

@router.get("/health")
async def health_check():
    """Verifica el estado del servicio"""
    return {
        "status": "healthy",
        "spark_initialized": analysis_service._spark_initialized,
        "books_analyzed": len(analysis_service.docs)
    }
