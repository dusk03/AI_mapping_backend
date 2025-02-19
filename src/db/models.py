from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime
from typing import Optional, List


class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = Field(default=False)
    password: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    conversations: List["Conversation"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Chatbot(SQLModel, table=True):
    __tablename__ = "chatbots"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str
    version: str
    description: Optional[str] = None
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    conversations: List["Conversation"] = Relationship(
        back_populates="chatbot", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<Chatbot {self.name}>"


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    chatbot_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="chatbots.uid")
    title: Optional[str] = None
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    user: Optional[User] = Relationship(back_populates="conversations")
    chatbot: Optional[Chatbot] = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(
        back_populates="conversation", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<Conversation {self.title}>"


class Message(SQLModel, table=True):
    __tablename__ = "messages"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    conversation_uid: Optional[uuid.UUID] = Field(
        default=None, foreign_key="conversations.uid"
    )
    sender: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))  # "user" or "bot"
    message: str
    timestamp: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    conversation: Optional[Conversation] = Relationship(back_populates="messages")

    def __repr__(self):
        return f"<Message by {self.sender}>"
