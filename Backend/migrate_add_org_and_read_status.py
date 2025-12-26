"""
Migration script to add Organization models and is_read field to Email.
Run this after updating models.
"""
import asyncio
from sqlalchemy import text
from app.db.session import engine
from app.db.models import Base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def migrate():
    async with engine.begin() as conn:
        logger.info("Creating organizations table...")
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS organizations (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name VARCHAR NOT NULL,
                plan_type VARCHAR DEFAULT 'free',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """))
        
        logger.info("Creating user_organizations table...")
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS user_organizations (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
                role VARCHAR NOT NULL DEFAULT 'member',
                joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                UNIQUE(user_id, organization_id)
            );
        """))
        
        logger.info("Adding is_read column to emails table...")
        await conn.execute(text("""
            ALTER TABLE emails 
            ADD COLUMN IF NOT EXISTS is_read BOOLEAN DEFAULT FALSE;
        """))
        
        logger.info("Adding name and avatar columns to users table...")
        await conn.execute(text("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS name VARCHAR,
            ADD COLUMN IF NOT EXISTS avatar VARCHAR;
        """))
        
        logger.info("Creating indexes...")
        await conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_user_organizations_user_id ON user_organizations(user_id);
            CREATE INDEX IF NOT EXISTS idx_user_organizations_org_id ON user_organizations(organization_id);
            CREATE INDEX IF NOT EXISTS idx_emails_is_read ON emails(is_read);
        """))
        
        logger.info("✅ Migration complete!")

if __name__ == "__main__":
    asyncio.run(migrate())

