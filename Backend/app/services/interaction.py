from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Interaction, Email
from app.schemas.interaction import InteractionCreate
import uuid
import logging

logger = logging.getLogger(__name__)

class InteractionService:
    async def create_interaction(self, db: AsyncSession, email_id: uuid.UUID, interaction_in: InteractionCreate):
        # 1. Verify email exists
        result = await db.execute(select(Email).where(Email.id == email_id))
        email = result.scalars().first()
        if not email:
            return None
        
        # 2. Create Interaction
        interaction = Interaction(
            email_id=email_id,
            action=interaction_in.action
        )
        db.add(interaction)
        await db.commit()
        await db.refresh(interaction)
        
        logger.info(f"Logged interaction '{interaction.action}' for email {email_id}")
        return interaction

interaction_service = InteractionService()
