import uuid
from fastapi import Depends
from src.db.main import get_session
from sqlmodel import select
from src.db.models import Conversation
from src.auth.dependencies import AccessTokenBearer
from sqlmodel.ext.asyncio.session import AsyncSession


async def check_conversation_owner(
    conversation_uid: uuid.UUID,
    user: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    """
    Lấy một conversation cụ thể theo UID và kiểm tra xem nó có thuộc về user không.
    """
    user_id = user["user"]["user_uid"]
    statement = select(Conversation).where(Conversation.uid == conversation_uid)
    result = await session.exec(statement)
    conversation = result.first()
    if not conversation:
        return None

    if str(conversation.user_uid) != user_id:
        return None

    return conversation
