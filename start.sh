#!/bin/bash
echo "Запускаю обновление системы..."
docker compose up --build -d
echo "Готово! Проверяю статус контейнеров:"
docker compose ps
