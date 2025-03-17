from kafka import KafkaProducer, KafkaConsumer
import os
import json
import datetime

kafka_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
kafka_topic = os.getenv("KAFKA_TOPIC", "my_topic")

producer = KafkaProducer(
    bootstrap_servers=kafka_servers,
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers=kafka_servers,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="latest"
)


def kafka_send(status, text):
    message_payload = {
        "status": status,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "message": text
    }
    producer.send(kafka_topic, message_payload)
    producer.flush()


def kafka_read():
    data = []
    for msg in consumer:
        data.append(msg.value)
    return data
