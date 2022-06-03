import asyncio
from typing import List
from fastapi import Depends
import uvloop
from fastapi import FastAPI, Request, status

from repos.mongo_repo import ConnectedMongoRepo
from entities import ConnectedOut, RealtimeConnected
from utils.mongo import MotorClient

from use_case import ConnectedUseCase

db = MotorClient()


async def on_startup() -> None:
    await db.connect_client()


async def on_shutdown() -> None:
    await db.close_client()


app = FastAPI(
    description="Whos is that motorcycle? It is a chopper...",
    version="0.0.1",
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
    contact={
        "name": "Rafal Kesik",
        "url": "https://www.linkedin.com/in/rafalkesik/",
        "email": "rafal.kesik@gmail.com",
    },
)

uvloop.install()

realtime_use_case = ConnectedUseCase(repo_adapter=ConnectedMongoRepo)


@app.get("/")
async def health_check(
    request: Request, use_case=Depends(realtime_use_case.get_db_client)
) -> dict:
    return {"message": "Hello, I am fine."}


@app.get("/connected/realtime/{handle_first}/{handle_second}", status_code=status.HTTP_200_OK)
async def connect_devs(
    handle_first: str,
    handle_second: str,
    use_case=Depends(realtime_use_case.get_db_client),
) -> RealtimeConnected:
    errors = []

    connected = await use_case.check_if_connected(
        handle_first, handle_second, errors=errors
    )

    # At that point we can say that if there are any errors we should brak a flow
    if errors:
        return {"errors": errors}  # TODO(rkesik): add proper status_code 404

    await use_case.register_connection(connected, handle_first, handle_second)
    
    #TODO(rkesik): we need to ensure proper statuses to be returned 200, 404...
    
    return RealtimeConnected(**connected.dict())


@app.get("/connected/register/{handle_first}/{handle_second}")
async def get_register(
    handle_first: str,
    handle_second: str,
    use_case=Depends(realtime_use_case.get_db_client),
) -> List[ConnectedOut]:
    return await use_case.get_registers(handle_first, handle_second)


if __name__ == "__main__":
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = "0.0.0.0:8080"
    # TODO: fill up config.toml
    # config.from_toml("config.toml")
    asyncio.run(serve(app, config))
