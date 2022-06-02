from typing import List
import datetime as dt
from pydantic import BaseModel, Field


class RealtimeOut(BaseModel):
    connected: bool
    organizations: List[str]


class RegisterOut(RealtimeOut):
    registered_at: dt.datetime = Field(default_factory=dt.datetime.now)
