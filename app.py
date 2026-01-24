from flask import Flask
import redis
import datetime

app = Flask(__name__)
cache = redis.Redis(host='my_secret_db', port=6379)

@app.route('/')
def hello():
    # Берем число из Redis и увеличиваем его
    count = cache.incr('hits')
    return f'''
    <html>
        <body style="text-align: center; font-family: sans-serif; margin-top: 50px; color: purple;">
            <h1>Привет из Docker! 🐳</h1>
            <p style="font-size: 24px;">Этот сайт работает на Python и Redis.</p>
            <div style="font-size: 48px; color: #007bff; font-weight: bold;">
             {UserWarning}brontozyabrjopa s ru4koi{count} раз
            </div>
        </body>
    </html>
    '''
@app.route('/i')
def i():
user_name = "BrontoDev"
    
    # Получаем текущее время
    now = datetime.datetime.now().strftime("%H:%M:%S")
    return f"""
        <h1>Хsрактеристики сервера</h1>
        <p>Текущее время на сервере: {now}</p>
	<p> разраб:{user_name}</p>
        <a href="/">Назад на главную</a>
    """
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
