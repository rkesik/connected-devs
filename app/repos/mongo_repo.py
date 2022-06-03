from typing import Optional, List

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
import datetime as dt
from entities import ConnectedOut, ConnectedIn
from pydantic import parse_obj_as


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
    async def save_register(
        cls, motor_db: AsyncIOMotorDatabase, connection: ConnectedIn
    ) -> ConnectedOut:
        collection: AsyncIOMotorCollection = await cls.get_collection(
            motor_db, "register"
        )
        data = connection.dict()
        data["registered_at"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        await collection.insert_one(data)
        return ConnectedOut(**data)

    @classmethod
    async def get_registers(
        cls, motor_db: AsyncIOMotorDatabase, handle_one: str, handle_two: str
    ) -> List[ConnectedOut]:
        collection: AsyncIOMotorCollection = await cls.get_collection(
            motor_db, "register"
        )
        # TODO(rkesik): ofc we need to add more control flow, like objects do not exists exists...
        cursor = collection.find({"devs": [handle_one, handle_two]})
        _all = []
        async for doc in cursor:
            _all.append(doc)
        return parse_obj_as(List[ConnectedOut], _all)
