# Используем легковесный базовый образ на Python 3.10 (можно указать 3.11 или др.)
FROM python:3.10-slim

# Чтобы apt-get не зависал на вопросах
ENV DEBIAN_FRONTEND=noninteractive

# Устанавливаем Chromium и chromedriver
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        chromium \
        chromium-driver \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Создаём рабочую директорию
WORKDIR /app

# Скопируем файлы зависимостей (если у вас есть requirements.txt)
COPY requirements.txt ./

# Создаем и активируем виртуальное окружение, затем устанавливаем зависимости
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем оставшийся проектный код в контейнер
COPY . /app
COPY .env /app/.env

# Запускаем ваш скрипт при старте контейнера
CMD ["venv/bin/python", "main.py", ">>" ,"/home/logs/app.log", "2>&1"]
