import os

import asyncio
from faststream import FastStream
from faststream.rabbit import RabbitBroker, ExchangeType, schemas, RabbitQueue, RabbitExchange
from faststream.security import SASLPlaintext

# get rabbitmq password fron environment variable:
RABBIT_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

async def main():
    
    # 定义与服务器上交换机参数一致的交换机
    exchange = RabbitExchange(
        name="test_exchange",
        type=ExchangeType.DIRECT,  # 请确保与服务器上的类型一致
        durable=True,
        auto_delete=False,
        passive=False,  # 如果交换机已存在，可以设为 True，如果要自动创建则设为 False
    )
    
    broker = RabbitBroker(
        host="192.168.1.5",
        port=5672,
        virtualhost="/",
        security=SASLPlaintext(
            username="david",
            password= RABBIT_PASSWORD,
        ),
        max_consumers=10, # Will take no more than 10 messages in advance (aka prefetch count)
    )
    app = FastStream(broker)

    @broker.subscriber("test_queue", exchange=exchange, retry=True)
    async def handle(msg):
        print(msg)

    await app.run()

if __name__ == "__main__":
    asyncio.run(main())
