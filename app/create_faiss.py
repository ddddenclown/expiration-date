import json
import numpy as np
import faiss
from openai import OpenAI
from typing import List, Dict, Any

from app.config import settings

API_KEY = settings.OPENAI_API_KEY


def load_products(file_path: str) -> List[Dict[str, Any]]:
    """Загружает товары из JSON файла"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def prepare_text_for_embedding(products: List[Dict[str, Any]]) -> List[str]:
    """Объединяет ItemName + Description в одну строку для каждого товара"""
    texts = []
    for product in products:
        # Объединяем ItemName и Description (если есть) в одну строку
        item_name = product.get('ItemName', '')
        description = product.get('Description', '')
        
        if description:
            combined_text = f"{item_name}. {description}"
        else:
            combined_text = item_name
        
        texts.append(combined_text)
    
    return texts

def get_embeddings_batch(texts: List[str], batch_size: int = 50) -> List[List[float]]:
    """Получает embeddings для текстов batch-запросами"""
    client = OpenAI(api_key=API_KEY)
    all_embeddings = []
    
    # Обрабатываем тексты батчами
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        print(f"Обрабатываю batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}")
        
        try:
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=batch_texts
            )
            
            batch_embeddings = [embedding.embedding for embedding in response.data]
            all_embeddings.extend(batch_embeddings)
            
        except Exception as e:
            print(f"Ошибка при получении embeddings для batch {i//batch_size + 1}: {e}")
            # В случае ошибки добавляем пустые embeddings
            empty_embedding = [0.0] * 1536  # размерность text-embedding-3-small
            all_embeddings.extend([empty_embedding] * len(batch_texts))
    
    return all_embeddings

def create_faiss_index(embeddings: List[List[float]], products: List[Dict[str, Any]]) -> None:
    """Создает FAISS индекс и сохраняет его на диск"""
    # Преобразуем в numpy.float32 сразу для всего массива
    embeddings_array = np.array(embeddings, dtype=np.float32)
    
    # Создаем простой FAISS индекс (IndexFlatL2)
    dimension = embeddings_array.shape[1]
    index = faiss.IndexFlatL2(dimension)
    
    # Добавляем векторы в индекс
    index.add(embeddings_array)
    
    # Сохраняем индекс на диск
    faiss.write_index(index, "app/products_index.faiss")
    
    # Сохраняем информацию о товарах для поиска
    products_info = []
    for i, product in enumerate(products):
        products_info.append({
            'index': i,
            'ItemName': product.get('ItemName', ''),
            'Description': product.get('Description', ''),
            'LifeTime': product.get('LifeTime', 0)
        })
    
    with open("app/products_info.json", 'w', encoding='utf-8') as f:
        json.dump(products_info, f, ensure_ascii=False, indent=2)
    
    print(f"FAISS индекс создан и сохранен:")
    print(f"- Размерность: {dimension}")
    print(f"- Количество товаров: {len(products)}")
    print(f"- Файлы: app/products_index.faiss, app/products_info.json")

def main():
    """Основная функция для создания FAISS индекса"""
    print("Начинаю создание FAISS индекса...")
    
    # Загружаем товары
    products = load_products("app/products.json")
    print(f"Загружено {len(products)} товаров")
    
    # Подготавливаем тексты для embedding
    texts = prepare_text_for_embedding(products)
    print(f"Подготовлено {len(texts)} текстов для embedding")
    
    # Получаем embeddings batch-запросами
    print("Получаю embeddings...")
    embeddings = get_embeddings_batch(texts, batch_size=50)
    print(f"Получено {len(embeddings)} embeddings")
    
    # Создаем FAISS индекс
    print("Создаю FAISS индекс...")
    create_faiss_index(embeddings, products)
    
    print("Готово! FAISS индекс успешно создан.")

if __name__ == "__main__":
    main()
