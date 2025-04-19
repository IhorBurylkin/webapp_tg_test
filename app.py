# app.py
from flask import Flask, jsonify, request, render_template
import os

app = Flask(__name__)

# Базовый URL вашего API (без слэша в конце), 
# например "https://aiassistantontelegrambot.uk"
API_BASE_URL = os.getenv('API_BASE_URL', '')

@app.route('/')
def index():
    # Передаём API_BASE_URL в шаблон
    return render_template('index.html', api_base_url=API_BASE_URL)

@app.route('/api/hello', methods=['POST'])
def api_hello():
    data = request.get_json(silent=True) or {}
    name = data.get('name', 'World')
    return jsonify({'message': f'Hello, {name}!'}), 200

# if __name__ == '__main__':
#     # Запускаем локально — всё равно облачный tunnel уже подхватит 5000 порт
#     app.run(host='127.0.0.1', port=5000)
