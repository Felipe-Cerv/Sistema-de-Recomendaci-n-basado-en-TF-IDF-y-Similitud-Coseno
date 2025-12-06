from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Backend - Sistema de Recomendación de Libros"
    API_V1_STR: str = "/api/v1"
    
    # Books & NLP
    BOOKS_RAW_PATH: str = "./data/raw_books"
    BOOKS_CLEAN_PATH: str = "./data/clean_books"
    NLTK_DATA_DIR: str = "./data/nltk_data"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
