from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient, AsyncIOMotorCollection
import entities


class MongoRepoBase:

    __db_name = "connected"

    @classmethod
    def connect(
        cls, client: AsyncIOMotorClient, db_name: Optional[str] = None
    ) -> AsyncIOMotorDatabase:
        db_name = db_name or cls.__db_name
        return client[db_name]

    @classmethod
    async def get_collection(
        cls, async_db: AsyncIOMotorDatabase, collection: str
    ) -> AsyncIOMotorCollection:
        return async_db[collection]


class ConnectedMongoRepo(MongoRepoBase):
    @classmethod
    async def create(
        cls,
        motor_db: AsyncIOMotorDatabase,
    ) -> entities.RegisterOut:
        ...

    @classmethod
    async def test(
        cls,
        motor_db: AsyncIOMotorDatabase,
    ) -> entities.RegisterOut:
        collection: AsyncIOMotorCollection = await cls.get_collection(motor_db, 'cibs')
        d = await collection.insert_one({'x':1 })