import os 

import asyncio    
from faststream import FastStream, Logger
from faststream.rabbit import ExchangeType, RabbitBroker, RabbitExchange, RabbitQueue
from faststream.security import SASLPlaintext

RABBIT_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

broker = RabbitBroker(
        host="192.168.35.8",
        port=5672,
        virtualhost="/",
        security=SASLPlaintext(
            username="david",
            password=RABBIT_PASSWORD,
        ),
        max_consumers=10, # Will take no more than 10 messages in advance (aka prefetch count)
)
    
app = FastStream(broker)

exch = RabbitExchange("topic_exchange_2024", auto_delete=False, type=ExchangeType.TOPIC)

queue_1 = RabbitQueue("test-queue-1", auto_delete=False, routing_key="*.info")
queue_2 = RabbitQueue("test-queue-2", auto_delete=False, routing_key="*.debug")


@broker.subscriber(queue_1, exch)
async def base_handler1(logger: Logger):
    print("base_handler1")
    logger.info("base_handler1")


@broker.subscriber(queue_1, exch)  # another service
async def base_handler2(logger: Logger):
    print("base_handler2")
    logger.info("base_handler2")


@broker.subscriber(queue_2, exch)
async def base_handler3(logger: Logger):
    print("base_handler3")
    logger.info("base_handler3")


@app.after_startup
async def send_messages():
    print("sending messages...")
    await broker.publish("test message 1", routing_key="logs.info", exchange=exch,  )
    await broker.publish("test message 2", routing_key="logs.info", exchange=exch,  )
    await broker.publish("test message 3", routing_key="logs.info", exchange=exch,  )
    await broker.publish("test message 4", routing_key="logs.debug", exchange=exch,  )
    
    
async def main():
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())
