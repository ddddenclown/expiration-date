from openai import OpenAI
import numpy as np
import faiss
import json
import os
from typing import Optional

from app.config import settings

API_KEY = settings.OPENAI_API_KEY

class ProductCRUD:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY)
        self.index = None
        self.products_info = []
        self._load_data()
    
    def _load_data(self):
        """Загружает FAISS индекс и информацию о товарах"""
        try:
            # Загружаем FAISS индекс
            index_path = "app/products_index.faiss"
            if os.path.exists(index_path):
                self.index = faiss.read_index(index_path)
                print(f"FAISS индекс загружен: {index_path}")
            else:
                print(f"FAISS индекс не найден: {index_path}")
                return
            
            # Загружаем информацию о товарах
            info_path = "app/products_info.json"
            if os.path.exists(info_path):
                with open(info_path, 'r', encoding='utf-8') as f:
                    self.products_info = json.load(f)
                print(f"Информация о товарах загружена: {info_path}")
            else:
                print(f"Информация о товарах не найдена: {info_path}")
                
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
    
    def get_query_embedding(self, query: str) -> Optional[np.ndarray]:
        """Получает embedding для поискового запроса"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=[query]
            )
            
            # Преобразуем в numpy.float32
            embedding = np.array(response.data[0].embedding, dtype=np.float32)
            return embedding
            
        except Exception as e:
            print(f"Ошибка при получении embedding для запроса: {e}")
            return None
    
    def get_shelf_life_by_name(self, product_name: str) -> Optional[int]:
        """Получает срок годности товара по названию"""
        if self.index is None or not self.products_info:
            return None
        
        # Получаем embedding для запроса
        query_embedding = self.get_query_embedding(product_name)
        if query_embedding is None:
            return None
        
        # Выполняем поиск по FAISS индексу
        query_embedding = query_embedding.reshape(1, -1)
        
        # Ищем ближайший вектор
        distances, indices = self.index.search(query_embedding, 1)
        
        # Возвращаем срок годности самого похожего товара
        if indices[0][0] < len(self.products_info):
            return self.products_info[indices[0][0]].get('LifeTime')
        
        return None