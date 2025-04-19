import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# ——————————————————————————————————————————————————————————————
# Логирование
# ——————————————————————————————————————————————————————————————
# создаём форматтер
formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
)

# вращающийся файл-логгер: max 10MB, хранить 5 ротаций
file_handler = RotatingFileHandler(
    "app.log", maxBytes=10*1024*1024, backupCount=5, encoding="utf-8"
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# подключаем к логгеру Flask
app.logger.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

# логируем все входящие запросы
@app.before_request
def log_request_info():
    app.logger.info(
        "%s %s %s — Headers: %s — Body: %s",
        request.remote_addr,
        request.method,
        request.path,
        dict(request.headers),
        request.get_data(as_text=True)
    )

# ——————————————————————————————————————————————————————————————
# Конфигурация приложения
# ——————————————————————————————————————————————————————————————
API_BASE_URL = os.getenv('API_BASE_URL', '')

@app.route('/')
def index():
    app.logger.info("Rendering index page, API_BASE_URL=%s", API_BASE_URL)
    return render_template('index.html', api_base_url=API_BASE_URL)

@app.route('/api/hello', methods=['POST'])
def api_hello():
    data = request.get_json(silent=True) or {}
    name = data.get('name', 'World')
    app.logger.info("Received hello request, name=%s", name)
    resp = {'message': f'Hello, {name}!'}
    app.logger.info("Responding: %s", resp)
    return jsonify(resp), 200

# ——————————————————————————————————————————————————————————————
if __name__ == "__main__":
    from waitress import serve
    app.logger.info("Starting Waitress on 127.0.0.1:5000")
    serve(app, host='127.0.0.1', port=5000)
