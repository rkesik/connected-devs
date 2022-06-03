from repos.mongo_repo import ConnectedMongoRepo
from repos.github import GitHubRepo
from repos.twitterrepo import TwiterRepo

from utils.mongo import MotorClient
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase

from entities import ConnectedOut, ConnectedIn


class ConnectedUseCase:
    def __init__(self, repo_adapter: ConnectedMongoRepo) -> None:
        self.__repo_adapter = repo_adapter
        self.__db: Optional[AsyncIOMotorDatabase] = None
        self.repo_github = GitHubRepo()
        self.repo_twiter = TwiterRepo()

    async def get_db_client(self):
        motor_client_instance = MotorClient()
        client = await motor_client_instance.get_db_client()
        self.__db = client["connected"]
        return self

    async def check_if_connected(
        self, handle_one: str, handle_two: str, errors: List[str] = None
    ) -> Optional[ConnectedOut]:
        orgs = await self.get_common_organizations(
            handle_one, handle_two, errors=errors
        )
        following = await self.are_devs_following_each_other(
            handle_one, handle_two, errors=errors
        )
        if errors:
            return False

        connection = ConnectedOut()
        # add date when that checking happended
        if following and orgs:
            connection.connected = True
            connection.organizations = orgs
        return connection

    async def get_common_organizations(
        self, handle_one: str, handle_two: str, errors: list = None
    ):
        # TODO(rkesik): handle_one and handle_two should be a list to be more generic
        first_org = self.repo_github.get_organizations(handle_one, errors=errors)
        second_org = self.repo_github.get_organizations(handle_two, errors=errors)
        return list(set(first_org) & set(second_org))

    async def are_devs_following_each_other(
        self, handle_one: str, handle_two: str, errors: list = None
    ):
        return True  # TODO(rkesik) just a stub for sake of assigment
        first_followers = self.repo_twiter.get_followers(handle_one, errors=errors)
        second_followers = self.repo_twiter.get_followers(handle_two, errors=errors)
        if handle_one in second_followers and handle_two in first_followers:
            return True
        return False

    async def register_connection(
        self, connected: ConnectedOut, handle_first: str, handle_second: str
    ) -> ConnectedOut:
        data_in = connected.dict()
        data_in["devs"] = [handle_first, handle_second]
        db_in = ConnectedIn(**data_in)
        await self.__repo_adapter.save_register(self.__db, db_in)
        return ConnectedOut(**connected.dict())

    async def get_registers(
        self, handle_first: str, handle_second: str
    ) -> List[ConnectedOut]:
        return await self.__repo_adapter.get_registers(
            self.__db, handle_first, handle_second
        )
