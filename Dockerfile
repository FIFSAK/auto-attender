FROM selenium/standalone-chrome:latest

USER root
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

WORKDIR /app

COPY . /app

RUN python3 -m venv venv
RUN . venv/bin/activate && pip install -r requirements.txt

CMD ["/app/venv/bin/python3", "main.py"]
