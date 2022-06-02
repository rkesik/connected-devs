import asyncio
from typing import List
from fastapi import Depends
import uvloop
from fastapi import FastAPI, Request

import repo
from entities import RealtimeOut, RegisterOut
from utils.mongo import MotorClient

from use_case import RegisterUseCase, RealtimeUseCase

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

# reqister_usecase = RegisterUseCase(repo_adapter=repo.ConnectedMongoRepo, db_client=db)
realtime_use_case = RealtimeUseCase(repo_adapter=repo.ConnectedMongoRepo)

@app.get("/")
async def health_check(request: Request, use_case=Depends(realtime_use_case.get_repo_client)) -> dict:
    await use_case.test()
    return {"message": "Hello, I am fine."}


@app.post("/connected/realtime/{first_dev}/{second_dev}")
async def connect_devs(handle_first: str, handle_second: str, ) -> RealtimeOut:
    ...

@app.post("/connected/register/{first_dev}/{second_dev}")
async def get_register(handle_first: str, handle_second: str) -> List[RegisterOut]:
    ...


if __name__ == "__main__":
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = "0.0.0.0:8080"
    # TODO: fill up config.toml
    # config.from_toml("config.toml")
    asyncio.run(serve(app, config))
