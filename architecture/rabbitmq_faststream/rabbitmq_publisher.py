import os

import asyncio
from faststream.rabbit import RabbitBroker, schemas, RabbitQueue
from faststream.security import SASLPlaintext

RABBIT_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

async def main():
    broker = RabbitBroker(
        host="192.168.1.5",
        port=5672,
        virtualhost="/",
        security=SASLPlaintext(
            username="david",
            password=RABBIT_PASSWORD,
        ),
        max_consumers=10, # Will take no more than 10 messages in advance (aka prefetch count)
    )
    await broker.connect()
    
    await broker.publish("Hello world!", "test_queue", exchange="test_exchange")


if __name__ == "__main__":
    asyncio.run(main())
