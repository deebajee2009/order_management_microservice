import uuid
import asyncio
import aio_pika

from config import config

MAX_RETRIES = config.MAX_RE
RETRY_DELAY = config.RETRY_DELAY
RPC_TIMEOUT = config.RPC_TIMEOUT
USER_ID_REQUEST_QUEUE = config.USER_ID_REQUEST_QUEUE

RABBITMQ_HOST = config.RABBITMQ_HOST
RABBITMQ_USER = config.RABBITMQ_USER
RABBITMQ_PASSWORD = config.RABBITMQ_PASSWORD

connection_uri = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}/"

async def get_user_id_from_users_service(phone_number: str):
    connection = None
    retry_count = 0
    while retry_count < MAX_RETRIES:
        retry_count += 1
        try:
            connection = await aio_pika.connect_robust(
                connection_uri
            )
            channel: aio_pika.abc.AbstractChannel = await connection.channel()
            # Enable publisher confirms so that the publish call waits for broker acknowledgment
            await channel.confirm_select()

            queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(USER_ID_REQUEST_QUEUE, durable=True)

            correlation_id = str(uuid.uuid4()) # Generate unique ID for request
            response_future: asyncio.Future = asyncio.Future()

            async def on_response(message: aio_pika.abc.AbstractIncomingMessage):
                try:
                    if message.correlation_id == correlation_id and not response_future.done():
                        response_future.set_result(message) # Set the future result when response arrives
                        await message.ack()
                except Exception as e:
                    await message.nack()
            callback_queue: aio_pika.abc.AbstractQueue = await channel.queue_declare(
                queue_name="", exclusive=True # Exclusive queue, auto-deleted when consumer cancelled
            )
            await callback_queue.consume(on_response, no_ack=False) # Consumer to receive response (no_ack for callback consumer in this example)

            await channel.default_exchange.publish(
                aio_pika.Message(
                    phone_number.encode(), # Send phone_number as message body
                    content_type='text/plain',
                    correlation_id=correlation_id,
                    reply_to=callback_queue.name, # Tell server where to send the response
                ),
                routing_key=USER_ID_REQUEST_QUEUE, # Route to the user ID request queue
            )

            try:
                response_message = await asyncio.wait_for(response_future, timeout=RPC_TIMEOUT) # Wait for response with timeout
                user_id_bytes = response_message.body
                user_id_str = user_id_bytes.decode() if user_id_bytes else None # Decode user_id from response

                return user_id_str
            except asyncio.TimeoutError:
                if retry_count < MAX_RETRIES:
                    await asyncio.sleep(RETRY_DELAY) # Wait before retrying
                continue # Retry from the beginning of the while loop

        except aio_pika.exceptions.AMQPConnectionError as e: # Catch connection errors specifically
            if retry_count < MAX_RETRIES:
                await asyncio.sleep(RETRY_DELAY) # Wait before retrying connection
            continue # Retry connection in the next loop iteration

        except Exception as e: # Catch other potential errors during RPC

            return None # Indicate error

        finally:
            if connection:
                await connection.close()
    return None # Indicate failure after max retries
