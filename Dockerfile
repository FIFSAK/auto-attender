# Используем базовый образ на основе Ubuntu
FROM ubuntu:latest

# Устанавливаем Python и другие зависимости
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv wget unzip curl && \
    apt-get clean

# Устанавливаем Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee -a /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    apt-get clean

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Создаем виртуальное окружение и устанавливаем зависимости
RUN python3 -m venv venv
RUN . venv/bin/activate && pip install -r requirements.txt

# Запуск приложения
CMD ["/app/venv/bin/python3", "main.py"]
