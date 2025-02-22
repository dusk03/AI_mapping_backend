from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime


class ConversationBase(BaseModel):
    title: Optional[str] = None
    user_uid: Optional[uuid.UUID]
    chatbot_uid: Optional[uuid.UUID]


class ConversationCreate(BaseModel):
    title: Optional[str] = None
    chatbot_uid: Optional[uuid.UUID]


class ConversationUpdate(BaseModel):
    title: Optional[str]


class ConversationResponse(ConversationBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
