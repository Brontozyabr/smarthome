FROM python:3.10-slim
ENV TZ=Europe/Warsaw
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app
# Копируем список библиотек
COPY requirements.txt .
# Устанавливаем их
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-u", "app.py"]
