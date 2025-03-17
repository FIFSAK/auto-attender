from kafka import KafkaProducer
import os
import json
import datetime


kafka_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
kafka_topic = os.getenv("KAFKA_TOPIC", "my_topic")

producer = KafkaProducer(
    bootstrap_servers=kafka_servers,
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)


def kafka_send(status, text):
    """
    Send a message to Kafka with:
      - status: string, e.g., "INFO", "ERROR", "STARTUP"
      - timestamp: current UTC time in ISO8601
      - message: main text content
    """
    message_payload = {
        "status": status,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "message": text
    }
    producer.send(kafka_topic, message_payload)
    producer.flush()