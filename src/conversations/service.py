from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from sqlmodel import select, desc
from src.db.models import Conversation
from src.conversations.schemas import ConversationCreate, ConversationUpdate
import uuid


class ConversationService:
    async def get_all_conversations(self, user_id: uuid.UUID, session: AsyncSession):
        """
        Lấy danh sách tất cả các conversation của một user, sắp xếp theo ngày tạo giảm dần.
        """
        statement = (
            select(Conversation)
            .where(Conversation.user_uid == user_id)
            .order_by(desc(Conversation.created_at))
        )
        result = await session.exec(statement)
        return result.all()

    async def get_conversation(
        self, user_id: uuid.UUID, conversation_uid: uuid.UUID, session: AsyncSession
    ):
        """
        Lấy một conversation cụ thể theo UID và kiểm tra xem nó có thuộc về user không.
        """
        statement = select(Conversation).where((Conversation.uid == conversation_uid))
        result = await session.exec(statement)
        conversation = result.first()
        if conversation.user_uid != user_id:
            return None
        return conversation if conversation else None

    async def create_conversation(
        self, user_uid, conversation_data: ConversationCreate, session: AsyncSession
    ):
        """
        Tạo một conversation mới.
        """
        conversation_data_dict = conversation_data.model_dump()
        conversation_data_dict["user_uid"] = user_uid
        new_conversation = Conversation(**conversation_data_dict)
        new_conversation.created_at = datetime.now()
        session.add(new_conversation)
        await session.commit()
        await session.refresh(new_conversation)  # Làm mới để trả về giá trị đầy đủ
        return new_conversation

    async def update_conversation_title(
        self,
        conversation: Conversation,
        conversation_data: ConversationUpdate,
        session: AsyncSession,
    ):

        if conversation_data.title:
            conversation.title = conversation_data.title

        # Commit changes to the database
        session.add(conversation)
        await session.commit()
        await session.refresh(
            conversation
        )  # Refresh to get the latest state from the DB

        return conversation

    async def delete_conversation(
        self,
        conversation: Conversation,
        session: AsyncSession,
    ) -> None:

        await session.delete(conversation)
        await session.commit()
