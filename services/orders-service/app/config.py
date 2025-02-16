import os


class Config:
    # MongoDB Configuration
    MONGO_HOST = os.getenv("MONGO_HOST")
    MONGO_PORT = os.getenv("MONGO_PORT")
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASS = os.getenv("MONGO_PASS")
    MONGO_DATABASE = os.getenv("MONGO_DATABASE")
    MONGO_COLLECTION_ORDERS = os.getenv("MONGO_COLLECTION_ORDERS")

    # RabbitMQ Configuration
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
    RABBITMQ_USER = os.getenv("RABBITMQ_USER")
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

    # RPC Configuration
    USER_ID_REQUEST_QUEUE = os.getenv("USER_ID_REQUEST_QUEUE")
    RPC_TIMEOUT = os.getenv("RPC_TIMEOUT") # seconds for RPC request timeout
    MAX_RETRIES = os.getenv("MAX_RETRIES")
    RETRY_DELAY = os.getenv("RETRY_DELAY")


config = Config()
