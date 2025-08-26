# Product Shelf Life API

API для поиска срока годности товаров по названию с использованием семантического поиска на базе OpenAI embeddings и FAISS индекса.

## Что делает проект

Проект предоставляет REST API для поиска товаров и получения информации о сроке их годности. Использует:
- **OpenAI embeddings** для семантического понимания названий товаров
- **FAISS индекс** для быстрого поиска похожих товаров
- **FastAPI** для backend API

## Структура проекта

```
semantic/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py              # Основной FastAPI файл
│   │       └── routers/
│   │           └── predict.py      # Роутер для API эндпоинтов
│   ├── crud/
│   │   └── product.py              # CRUD операции для товаров
│   ├── schemas/
│   │   └── product.py              # Pydantic модели данных
│   ├── products.json                # Исходные данные о товарах
│   ├── products_info.json           # Обработанные данные для индекса
│   ├── products_index.faiss        # FAISS индекс для поиска
│   └── create_faiss.py             # Скрипт создания FAISS индекса
├── requirements.txt                  # Зависимости Python
└── README.md                        # Этот файл
```

## API эндпоинты

- **GET** `/` - Проверка работоспособности API
- **GET** `/search/shelf-life/{product_name}` - Получение срока годности товара по названию
- **GET** `/docs` - Автоматическая документация Swagger UI

## Как запускать

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Создание FAISS индекса (если еще не создан)
```bash
cd app
python create_faiss.py
```

### 3. Запуск API сервера

#### Вариант 1: Из корневой папки проекта (рекомендуется)
```bash
cd C:\Users\Дмитрий\Desktop\job\semantic
python -m app.api.v1.api
```

#### Вариант 2: Через uvicorn
```bash
cd C:\Users\Дмитрий\Desktop\job\semantic
uvicorn app.api.v1.api:app --host 0.0.0.0 --port 8007 --reload
```

#### Вариант 3: Создать main.py в корне
Создайте файл `main.py` в корневой папке:
```python
from app.api.v1.api import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)
```

И запускайте:
```bash
python main.py
```

## Пример использования

После запуска сервера на порту 8007:

```bash
# Получить срок годности товара
curl "http://localhost:8007/search/shelf-life/чай%20травяной"

# Ответ
{
  "shelf_life_days": 365
}
```

## Важные замечания

- **Запускать нужно из корневой папки проекта** (где находится папка `app`)
- Убедитесь, что FAISS индекс создан перед запуском API
- API ключ OpenAI должен быть настроен в `app/crud/product.py`
- Сервер запускается на порту 8007
