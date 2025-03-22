FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Almaty

# Установка часового пояса
RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

# Установка Chromium и logrotate
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        chromium \
        chromium-driver \
        logrotate \
        cron \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Работаем из папки приложения
WORKDIR /app

COPY requirements.txt ./
RUN python -m venv venv && \
    ./venv/bin/pip install --upgrade pip && \
    ./venv/bin/pip install -r requirements.txt

COPY . /app
COPY .env /app/.env
COPY logrotate.conf /etc/logrotate.d/monitoring
COPY crontab.txt /etc/cron.d/logrotate-cron
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh && \
    chmod 0644 /etc/cron.d/logrotate-cron && \
    crontab /etc/cron.d/logrotate-cron && \
    mkdir -p /home/logs && touch /home/logs/app.log && chmod 666 /home/logs/app.log

CMD ["/app/entrypoint.sh"]
