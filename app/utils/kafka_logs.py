from aiokafka import AIOKafkaProducer
from pydantic import KafkaDsn
import json
from config import settings
from datetime import datetime
from functools import wraps
from typing import Callable, Any

class KafkaLogger:
    def __init__(self, kafka_dsn: KafkaDsn, topic: str):
        self.servers = kafka_dsn.host + ":" + str(kafka_dsn.port)
        self.topic = topic
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=self.servers)
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def log(self, action: str):
        if not self.producer:
            raise Exception("Kafka producer not started")
        print(action)
        message = {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        }
        await self.producer.send_and_wait(self.topic, json.dumps(message).encode("utf-8"))

kafka_logger = KafkaLogger(settings.kafka.bootstrap_servers, settings.kafka.topic)
print("kafka url:", kafka_logger.servers)


def kafka_log_action(action: str):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            response = await func(*args, **kwargs)
            
            try:
                await kafka_logger.log(action=action)
            except Exception as e:
                print(f"Failed to send log to Kafka: {e}")

            return response
        return wrapper
    return decorator