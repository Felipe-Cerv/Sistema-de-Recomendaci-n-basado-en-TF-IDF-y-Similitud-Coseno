import os
import math
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from pyspark.sql import SparkSession
from app.core.config import settings

class BookAnalysisService:
    """Servicio para análisis TF-IDF y recomendaciones con Spark"""
    
    def __init__(self):
        self.books_clean_path = Path(settings.BOOKS_CLEAN_PATH)
        self.spark = None
        self.sc = None
        self.docs = {}
        self._spark_initialized = False
    
    def _init_spark(self):
        """Inicializa SparkSession de forma lazy"""
        if not self._spark_initialized:
            try:
                import os
                import sys
                os.environ['PYSPARK_PYTHON'] = sys.executable
                os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
                
                self.spark = SparkSession.builder \
                    .appName("BookRecommender") \
                    .master("local[2]") \
                    .config("spark.sql.shuffle.partitions", "4") \
                    .config("spark.driver.memory", "1g") \
                    .config("spark.executor.memory", "1g") \
                    .config("spark.driver.host", "localhost") \
                    .config("spark.driver.bindAddress", "127.0.0.1") \
                    .config("spark.ui.enabled", "false") \
                    .config("spark.python.worker.reuse", "false") \
                    .getOrCreate()
                
                self.sc = self.spark.sparkContext
                self.sc.setLogLevel("ERROR")
                self._spark_initialized = True
            except Exception as e:
                raise RuntimeError(f"Error inicializando Spark. Asegúrate de tener Java 8+ instalado: {str(e)}")
    
    def load_and_analyze(self) -> bool:
        """Carga documentos y calcula TF-IDF"""
        # Inicializar Spark solo cuando se necesite
        self._init_spark()
        
        clean_books = [a for a in os.listdir(str(self.books_clean_path)) if a.endswith(".txt")]
        
        if not clean_books:
            return False
        
        documentos = []
        for archivo in clean_books:
            ruta = str(self.books_clean_path / archivo)
            try:
                with open(ruta, encoding="utf-8") as f:
                    texto = f.read()
            except:
                with open(ruta, "rb") as f:
                    texto = f.read().decode("utf-8", errors="ignore")
            documentos.append((ruta, texto.split()))
        
        N = len(documentos)
        rdd = self.sc.parallelize(documentos, 2)
        
        # Cálculo TF
        pairs = rdd.flatMap(lambda x: [((x[0], palabra), 1) for palabra in x[1]])
        tf = pairs.reduceByKey(lambda a, b: a + b)
        
        # Cálculo DF
        palabra_doc = tf.map(lambda x: (x[0][1], x[0][0])).distinct()
        df_rdd = palabra_doc.groupByKey().mapValues(lambda docs: len(list(docs)))
        df_dict = dict(df_rdd.collect())
        df_bc = self.sc.broadcast(df_dict)
        
        # Cálculo TF-IDF
        N_docs = float(N)
        tfidf = tf.map(lambda x: (
            x[0][0],
            x[0][1],
            x[1] * math.log(N_docs / df_bc.value.get(x[0][1], N_docs))
        ))
        
        # Agrupar vectores
        doc_vectors = tfidf.map(lambda x: (x[0], (x[1], x[2]))) \
                           .groupByKey() \
                           .mapValues(list)
        
        self.docs = dict(doc_vectors.collect())
        return True
    
    def coseno(self, vec1: List[Tuple], vec2: List[Tuple]) -> float:
        """Calcula similitud coseno entre dos vectores"""
        d1 = dict(vec1)
        d2 = dict(vec2)
        
        inter = set(d1.keys()) & set(d2.keys())
        if not inter:
            return 0.0
        
        num = sum(d1[w] * d2[w] for w in inter)
        mag1 = math.sqrt(sum(v*v for v in d1.values()))
        mag2 = math.sqrt(sum(v*v for v in d2.values()))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return num / (mag1 * mag2)
    
    def get_recommendations(self, doc_path: str, k: int = 5) -> List[Tuple[str, float]]:
        """Obtiene k recomendaciones para un documento"""
        if not self.docs:
            self.load_and_analyze()
        
        origen = self.docs.get(doc_path, [])
        if not origen:
            return []
        
        sims = [(d, self.coseno(origen, v)) for d, v in self.docs.items() if d != doc_path]
        sims = sorted(sims, key=lambda x: x[1], reverse=True)
        return sims[:k]
    
    def get_summary(self, doc_path: str, top: int = 20) -> str:
        """Obtiene resumen de palabras principales usando TF-IDF"""
        if not self.docs:
            self.load_and_analyze()
        
        doc_vector = self.docs.get(doc_path, [])
        if not doc_vector:
            return ""
        
        orden = sorted(doc_vector, key=lambda x: x[1], reverse=True)
        mejores = [pal for pal, peso in orden[:top]]
        return " ".join(mejores)
    
    def get_top_words(self, doc_path: str, top: int = 20) -> List[Tuple[str, float]]:
        """Obtiene las palabras principales con sus pesos TF-IDF"""
        if not self.docs:
            self.load_and_analyze()
        
        doc_vector = self.docs.get(doc_path, [])
        if not doc_vector:
            return []
        
        orden = sorted(doc_vector, key=lambda x: x[1], reverse=True)
        return [(pal, round(peso, 4)) for pal, peso in orden[:top]]
    
    def get_book_path(self, book_name: str) -> Optional[str]:
        """Encuentra la ruta completa de un libro por nombre"""
        full_path = str(self.books_clean_path / book_name)
        if full_path in self.docs:
            return full_path
        
        # Buscar por nombre parcial
        for doc_path in self.docs.keys():
            if book_name in doc_path or os.path.basename(doc_path) == book_name:
                return doc_path
        return None
    
    def get_all_books(self) -> List[str]:
        """Obtiene lista de todos los libros analizados"""
        return [os.path.basename(path) for path in self.docs.keys()]
    
    def stop_spark(self):
        """Detiene SparkSession"""
        if self.spark:
            self.spark.stop()
