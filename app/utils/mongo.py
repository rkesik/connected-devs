import ssl
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient


# TODO(rkesik): configuration details can be places in some config.yaml for example
# ideally passed form upper layers..
DB_NAME = "connected"
MONGO_DETAILS = f"mongodb://172.17.0.1:27017/{DB_NAME}"


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MotorClient(metaclass=SingletonMeta):
    def __init__(self):
        self.motor_client: Optional[AsyncIOMotorClient] = None

    def __create_client(self) -> AsyncIOMotorClient:
        self.motor_client = AsyncIOMotorClient(MONGO_DETAILS)
        return self.motor_client

    async def get_db_client(self) -> AsyncIOMotorClient:
        """Return database client instance."""
        return self.motor_client or self.__create_client()

    async def connect_client(self) -> AsyncIOMotorClient:
        """Create database connection."""
        if not self.motor_client:
            self.motor_client = self.__create_client()

    async def close_client(self):
        """Close database connection."""
        if self.motor_client:
            self.motor_client.close()
