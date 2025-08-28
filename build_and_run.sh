#!/bin/bash
set -e

# Останавливаем и удаляем существующий контейнер если он есть
docker stop fastapi-faiss || true
docker rm fastapi-faiss || true

# Собираем Docker образ
docker build -t fastapi-faiss .

# Запускаем Docker контейнер с меткой ветки и портом 8007
docker run --label branch=Dima_branch --restart unless-stopped -d -p 8007:8007 -e OPENAI_API_KEY="$OPENAI_API_KEY" --name fastapi-faiss fastapi-faiss
