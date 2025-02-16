import asyncio
import aio_pika

from config import config
from database import get_db

collection = config.MONGO_COLLECTION_USERS
db = get_db()

MAX_RETRIES = config.MAX_RETRIES # Maximum number of retries
RETRY_DELAY = config.RETRY_DELAY # Initial delay between retries in seconds
USER_ID_REQUEST_QUEUE = config.USER_ID_REQUEST_QUEUE

RABBITMQ_HOST = config.RABBITMQ_HOST
RABBITMQ_USER = config.RABBITMQ_USER
RABBITMQ_PASSWORD = config.RABBITMQ_PASSWORD

connection_uri = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}/"

# RabbitMQ RPC Server
async def consume_user_id_requests():
    connection = None
    try:
        connection = await aio_pika.connect_robust(
            connection_uri
        )
        channel: aio_pika.abc.AbstractChannel = await connection.channel()
        await channel.declare_queue(USER_ID_REQUEST_QUEUE, durable=True)

        async def on_message(message: aio_pika.abc.AbstractIncomingMessage):
            retry_count = 0
            while retry_count < MAX_RETRIES:
                try:
                    async with message.process(ignore_processed=True):
                        phone_number = message.body.decode()
                        user = await db[collection].find_one({"phone_number": phone_number}) # Search by name (username)
                        user_id = str(user["_id"]) if user else None
                        reply = str(user_id).encode() if user_id else b"" # Send user_id as bytes
                        await message.reply(body=reply)
                        # Manually acknowledge the message
                        await message.ack()
                        break  # Break the retry loop on success
                except Exception as e:
                    retry_count += 1
                    await asyncio.sleep(RETRY_DELAY)  # Exponential backoff
            if retry_count >= MAX_RETRIES:
                await message.nack(requeue=False)  # Reject the message after max retries without requeuing

        await channel.basic_qos(prefetch_count=1) # Fair dispatch, only process one message at a time
        await channel.consume(USER_ID_REQUEST_QUEUE, on_message)
        await asyncio.Future() # Keep consumer running forever

    except Exception as e:
        print(f"Error connecting to RabbitMQ or consuming messages: {e}")
    finally:
        if connection:
            await connection.close()
