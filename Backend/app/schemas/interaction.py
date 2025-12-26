from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Literal

class InteractionCreate(BaseModel):
    action: Literal['open', 'reply', 'archive', 'star']

class InteractionResponse(BaseModel):
    id: UUID4
    email_id: UUID4
    action: str
    created_at: datetime

    class Config:
        from_attributes = True
