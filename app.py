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
    fields = {
        'title': 'Трекер расходов',
        'date_label': 'Дата',
        'date_error': 'Выберите дату',
        'time_label': 'Время',
        'time_error': 'Укажите время',
        'store_label': 'Магазин',
        'store_error': 'Укажите название магазина',
        'product_label': 'Товары',
        'product_placeholder': 'Введите список покупок',
        'product_error': 'Укажите хотя бы один товар',
        'total_label': 'Сумма',
        'total_error': 'Укажите сумму',
        'currency_label': 'Валюта',
        'currency_select': 'Выберите валюту',
        'currency_error': 'Выберите валюту'
    }
    
    buttons = {
        'submit': 'Отправить'
    }
    
    return render_template('index.html', 
                          fields=fields, 
                          buttons=buttons, 
                          api_base_url=API_BASE_URL)

@app.route('/api/submit', methods=['GET'])
def api_submit():
    # Extract parameters from request
    date = request.args.get('date')
    time = request.args.get('time')
    store = request.args.get('store')
    product = request.args.get('product')
    total = request.args.get('total')
    currency = request.args.get('currency')
    chat_id = request.args.get('chat_id')
    
    # Log received data
    app.logger.info(
        "Received expense submission - Date: %s, Time: %s, Store: %s, "
        "Product: %s, Total: %s %s, Chat ID: %s",
        date, time, store, product, total, currency, chat_id
    )
    
    # Here you would typically process the data (save to DB, etc.)
    # ...
    
    # Return success response
    return jsonify({
        'success': True,
        'message': 'Данные успешно получены'
    }), 200

# ——————————————————————————————————————————————————————————————
if __name__ == "__main__":
    from waitress import serve
    app.logger.info("Starting Waitress on 127.0.0.1:5000")
    serve(app, host='127.0.0.1', port=5000)
