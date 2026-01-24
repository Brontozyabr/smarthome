FROM python:3.10-slim
WORKDIR /app
# Копируем список библиотек
COPY requirements.txt .
# Устанавливаем их
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python", "-u", "app.py"]
