from typing import List, Optional
import datetime as dt
from pydantic import BaseModel, Field


class Connected(BaseModel):
    connected: bool = False
    organizations: Optional[List[str]]


class RealtimeConnected(Connected):
    connected: bool
    organizations: Optional[List[str]]


class ConnectedIn(Connected):
    devs: List[str]


class ConnectedOut(Connected):
    registered_at: dt.datetime = Field(default_factory=dt.datetime.now)
