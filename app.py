from flask import Flask
import redis
import datetime
import time

app = Flask(__name__)
cache = redis.Redis(
    host='my_secret_db',
      port=6379,
      socket_timeout=0.1,
      socket_connect_timeout=0.1,
      retry_on_timeout=False,
      health_check_interval=0
)

@app.route('/')
def hello():
    try:
    # Берем число из Redis и увеличиваем его
        count = cache.incr('hits')
        db_status = f"База данных работает! Посещений: {count}"
    except redis.exceptions.ConnectionError:
        db_status = "База данных временно недоступна (но я живой!)"
    return f'''
    <html>
        <body style="text-align: center; font-family: sans-serif; margin-top: 50px;">
            <h1>Привет из Docker! 🐳</h1>
            <p>{db_status}</p>
            <br>
            <a href="/info">Посмотреть характеристики сервера</a>
        </body>
    </html>
    '''
    return f'''
    <html>
        <body style="text-align: center; font-family: sans-serif; margin-top: 50px; color: purple;">
            <h1>Привет из Docker! 🐳</h1>
            <p style="font-size: 24px;">Этот сайт работает на Python и Redis.</p>
            <div style="font-size: 48px; color: #007bff; font-weight: bold;">
             {UserWarning} ты заебал эту страничку уже {count} раз!
             <a href="/info">вперде на главную</a>
            </div>
        </body>
    </html>
    '''
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
