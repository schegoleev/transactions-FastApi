import asyncio
import aiormq

RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"
async def create_connection():

    connection = await aiormq.connect(f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@rabbitmq/")
    channel = await connection.channel()

    return channel