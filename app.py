from flask import Flask, render_template, redirect, url_for, request
import redis
import datetime
app = Flask(__name__)
cache = redis.Redis(
    host='my_secret_db',
    port=6379, 
    socket_timeout=0.1,           # Ждать ответа всего 100мс
    socket_connect_timeout=0.1,   # Ждать соединения всего 100мс
    retry_on_timeout=False,       # Не повторять при ошибке
    health_check_interval=0       # Отключить фоновые проверки
)
def add_event(message):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    event_text = f"[{now}] {message}"
    # lpush добавляет событие в начало списка 'history'
    cache.lpush('history', event_text)
    # Ограничиваем список последними 10 записями
    cache.ltrim('history', 0, 9)

@app.route('/')
def hello():
    try:
        count = cache.incr('hits')
        # Читаем состояние света из Redis (по умолчанию 'ВЫКЛ')
        light = cache.get('light_state')
        light_status = light.decode('utf-8') if light else "ВЫКЛ"
        status = f"Система онлайн. Посещений: {count}"

        #1. ЗАБИРАЕМ ИСТОРИЮ ИЗ REDIS
        history_raw = cache.lrange('history', 0, -1)
        # 2. ДЕКОДИРУЕМ ИЗ БАЙТОВ В ТЕКСТ
        history = [event.decode('utf-8') for event in history_raw]

    except Exception:
        status = "База данных недоступна"
        light_status = "Н/Д"
        history = []
    
    return render_template('index.html', db_status=status, light_status=light_status, history=history)

@app.route('/toggle_light', methods=['POST'])
def toggle_light():
    try:
        current = cache.get('light_state')
        new_state = "ВЫКЛ" if current and current.decode('utf-8') == "ВКЛ" else "ВКЛ"
        cache.set('light_state', new_state)
        # ВОТ ЭТА СТРОЧКА ДОЛЖНА БЫТЬ ТУТ:
        add_event(f"Свет переключен на {new_state}")
    except Exception as e:
        print(f"Ошибка в Redis: {e}") # Это поможет увидеть ошибку в терминале
    return redirect(url_for('hello'))

@app.route('/info')
def info():
    user_name = "BrontoDev"
    
    # Получаем текущий час (число от 0 до 23)
    current_hour = datetime.datetime.now().hour
    
    # Логика выбора приветствия
    if 5 <= current_hour < 12:
        greeting = "Доброе утро"
    elif 12 <= current_hour < 18:
        greeting = "Добрый день"
    elif 18 <= current_hour < 23:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    now = datetime.datetime.now().strftime("%H:%M:%S")
    
    return f"""
        <h1>Характеристики сервера</h1>
        <p>{greeting}, {user_name}!</p>
        <p>Текущее время на сервере: {now}</p>
        <a href="/">Назад на главную</a>
    """
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
