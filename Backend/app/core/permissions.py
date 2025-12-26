from functools import wraps
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.db.models import User, UserOrganization, OrganizationRole, Account
from app.db.session import get_db
from app.core.auth import get_current_user
from typing import Optional

PERMISSIONS = {
    "read_emails": [OrganizationRole.owner, OrganizationRole.admin, OrganizationRole.member, OrganizationRole.viewer],
    "write_emails": [OrganizationRole.owner, OrganizationRole.admin, OrganizationRole.member],
    "manage_members": [OrganizationRole.owner, OrganizationRole.admin],
    "manage_organization": [OrganizationRole.owner],
}

def require_permission(permission: str, organization_id: Optional[str] = None):
    """
    Decorator to require a specific permission.
    If organization_id is provided, checks user's role in that organization.
    Otherwise, checks if user has the permission in any organization.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            db: AsyncSession = kwargs.get("db") or next((arg for arg in args if isinstance(arg, AsyncSession)), None)
            user: User = kwargs.get("user") or next((arg for arg in args if isinstance(arg, User)), None)
            
            if not user:
                user = await get_current_user(kwargs.get("credentials"), db)
            
            if not db:
                db = next((arg for arg in args if isinstance(arg, AsyncSession)), None) or await get_db().__anext__()
            
            allowed_roles = PERMISSIONS.get(permission, [])
            
            if organization_id:
                stmt = select(UserOrganization).where(
                    and_(
                        UserOrganization.user_id == user.id,
                        UserOrganization.organization_id == organization_id
                    )
                )
                result = await db.execute(stmt)
                user_org = result.scalars().first()
                
                if not user_org or user_org.role not in allowed_roles:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"You don't have permission to {permission}"
                    )
            else:
                stmt = select(UserOrganization).where(UserOrganization.user_id == user.id)
                result = await db.execute(stmt)
                user_orgs = result.scalars().all()
                
                has_permission = any(uo.role in allowed_roles for uo in user_orgs)
                if not has_permission and not user_orgs:
                    has_permission = True
                
                if not has_permission:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"You don't have permission to {permission}"
                    )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

async def get_user_organization(
    user: User,
    organization_id: str,
    db: AsyncSession
) -> Optional[UserOrganization]:
    """
    Get user's organization membership.
    """
    stmt = select(UserOrganization).where(
        and_(
            UserOrganization.user_id == user.id,
            UserOrganization.organization_id == organization_id
        )
    )
    result = await db.execute(stmt)
    return result.scalars().first()

async def filter_emails_by_organization(
    user: User,
    db: AsyncSession
):
    """
    Helper to filter emails by user's organization memberships.
    Returns a query filter that restricts emails to those accessible by the user's organizations.
    """
    from app.db.models import Account, Email
    
    stmt_orgs = select(UserOrganization).where(UserOrganization.user_id == user.id)
    result = await db.execute(stmt_orgs)
    user_orgs = result.scalars().all()
    
    if not user_orgs:
        org_user_ids = [user.id]
    else:
        org_ids = [uo.organization_id for uo in user_orgs]
        stmt_users = select(UserOrganization.user_id).where(
            UserOrganization.organization_id.in_(org_ids)
        )
        result_users = await db.execute(stmt_users)
        org_user_ids = [uid for uid in result_users.scalars().all()]
    
    stmt_accounts = select(Account.id).where(Account.user_id.in_(org_user_ids))
    result_accounts = await db.execute(stmt_accounts)
    account_ids = [aid for aid in result_accounts.scalars().all()]
    
    return Email.account_id.in_(account_ids)

