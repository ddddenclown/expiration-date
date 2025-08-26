#!/bin/bash
set -euo pipefail

# --------------------------
# Настройки
# --------------------------
IMAGE_NAME="fastapi-faiss"
CONTAINER_NAME="fastapi-faiss-container"
PORT=8007
ENV_FILE=".env"

# --------------------------
# Функции
# --------------------------

function check_requirements() {
    # Проверка Docker
    if ! command -v docker &>/dev/null; then
        echo "❌ Docker не установлен! Установи Docker и повтори попытку."
        exit 1
    fi

    # Проверка запуска демона
    if ! docker info &>/dev/null; then
        echo "❌ Docker daemon не запущен! Запусти Docker Desktop/службу."
        exit 1
    fi
}

function build_image() {
    echo ">>> Сборка Docker-образа: $IMAGE_NAME"
    docker build -t "$IMAGE_NAME" .
}

function remove_old_container() {
    if docker ps -a --format '{{.Names}}' | grep -Eq "^${CONTAINER_NAME}\$"; then
        echo ">>> Остановка и удаление старого контейнера: $CONTAINER_NAME"
        docker rm -f "$CONTAINER_NAME"
    fi
}

function run_container() {
    echo ">>> Запуск контейнера: $CONTAINER_NAME"
    if [[ -f "$ENV_FILE" ]]; then
        docker run -d \
            --name "$CONTAINER_NAME" \
            --env-file "$ENV_FILE" \
            -p "$PORT:$PORT" \
            "$IMAGE_NAME"
    else
        docker run -d \
            --name "$CONTAINER_NAME" \
            -p "$PORT:$PORT" \
            "$IMAGE_NAME"
    fi
}

function show_status() {
    echo ">>> Запущенные контейнеры:"
    docker ps --filter "name=$CONTAINER_NAME"
    echo "✅ Готово! FastAPI доступен по адресу: http://localhost:${PORT}/docs"
}

# --------------------------
# Основной скрипт
# --------------------------

check_requirements
build_image
remove_old_container
run_container
show_status
