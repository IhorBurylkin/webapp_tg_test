# --- Стадия сборки (опционально) ---
    FROM python:3.12-slim AS builder
    WORKDIR /app
    
    # Копируем и ставим зависимости в user‑директорию
    COPY requirements.txt .
    RUN pip install --user --no-cache-dir -r requirements.txt
    
    # --- Финальный образ ---
    FROM python:3.12-slim
    WORKDIR /app
    
    # Добавляем bin‑директорию пользователя в PATH
    ENV PATH=/root/.local/bin:$PATH
    
    # Копируем пакеты из билдера и исходники
    COPY --from=builder /root/.local /root/.local
    COPY . .
    
    # Открываем порт
    EXPOSE 5000
    
    # По умолчанию запускаем Uvicorn
    CMD ["uvicorn", "asgi:asgi_app", "--host", "0.0.0.0", "--port", "5000"]
    