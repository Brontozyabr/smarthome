#!/bin/bash
docker compose up --build -d
echo "Система запущена!"
docker image prune -f  # Эта команда удалит старые версии образов, которые больше не нужны