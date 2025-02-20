from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class ChatbotBase(BaseModel):
    name: str
    version: str
    description: Optional[str]


class ChatbotCreate(ChatbotBase):
    pass


class ChatbotUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ChatbotResponse(ChatbotBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
