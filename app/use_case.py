
from repo import ConnectedMongoRepo
from utils.mongo import MotorClient
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase


class RealtimeUseCase:
    def __init__(self, repo_adapter: ConnectedMongoRepo) -> None:
        self.__repo_adapter = repo_adapter
        self.__db: Optional[AsyncIOMotorDatabase] = None

    async def get_repo_client(self):
        motor_client_instance = MotorClient()
        client = await motor_client_instance.get_db_client()
        self.__db = client['connections']
        return self

    async def test(self):
        await self.__repo_adapter.test(self.__db)


class RegisterUseCase:
    ...
