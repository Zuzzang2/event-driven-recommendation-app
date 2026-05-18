from typing import Literal
from pydantic import BaseModel


class EventCreate(BaseModel):
    user_id: str
    item_id: str
    event_type: Literal["view", "click"]


class EventResponse(BaseModel):
    id: int
    user_id: str
    item_id: str
    event_type: str
