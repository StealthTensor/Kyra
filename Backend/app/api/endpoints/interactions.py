from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.interaction import InteractionCreate, InteractionResponse
from app.services.interaction import interaction_service
import uuid

router = APIRouter()

@router.post("/emails/{email_id}/interaction", response_model=InteractionResponse)
async def log_interaction(
    email_id: uuid.UUID,
    interaction_in: InteractionCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Log a user interaction (open, reply, archive, star) for a specific email.
    """
    interaction = await interaction_service.create_interaction(db, email_id, interaction_in)
    if not interaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )
    return interaction
