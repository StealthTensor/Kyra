from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.db.session import get_db
from app.db.models import User, Organization, UserOrganization, OrganizationRole
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from app.core.auth import get_current_user

router = APIRouter()

class OrganizationCreate(BaseModel):
    name: str
    plan_type: str = "free"

class OrganizationMember(BaseModel):
    user_id: str
    role: str

class OrganizationMemberUpdate(BaseModel):
    role: str

@router.get("/")
async def list_organizations(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List all organizations the current user belongs to.
    """
    try:
        stmt = select(UserOrganization).where(UserOrganization.user_id == user.id)
        result = await db.execute(stmt)
        user_orgs = result.scalars().all()
        
        organizations = []
        for uo in user_orgs:
            org = uo.organization
            organizations.append({
                "id": str(org.id),
                "name": org.name,
                "plan_type": org.plan_type,
                "role": uo.role.value,
                "joined_at": uo.joined_at.isoformat() if uo.joined_at else None
            })
        
        return organizations
    except Exception as e:
        print(f"Error listing organizations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_organization(
    org_data: OrganizationCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new organization and add the current user as owner.
    """
    try:
        new_org = Organization(
            name=org_data.name,
            plan_type=org_data.plan_type
        )
        db.add(new_org)
        await db.flush()
        
        user_org = UserOrganization(
            user_id=user.id,
            organization_id=new_org.id,
            role=OrganizationRole.owner
        )
        db.add(user_org)
        await db.commit()
        await db.refresh(new_org)
        
        return {
            "id": str(new_org.id),
            "name": new_org.name,
            "plan_type": new_org.plan_type,
            "role": "owner"
        }
    except Exception as e:
        print(f"Error creating organization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{org_id}/members")
async def list_members(
    org_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List all members of an organization.
    """
    try:
        stmt = select(UserOrganization).where(
            and_(
                UserOrganization.organization_id == org_id,
                UserOrganization.user_id == user.id
            )
        )
        result = await db.execute(stmt)
        user_org = result.scalars().first()
        
        if not user_org:
            raise HTTPException(status_code=403, detail="You are not a member of this organization")
        
        stmt_members = select(UserOrganization, User).join(User).where(
            UserOrganization.organization_id == org_id
        )
        result_members = await db.execute(stmt_members)
        members_data = result_members.all()
        
        members = []
        for uo, u in members_data:
            members.append({
                "user_id": str(u.id),
                "email": u.email,
                "name": u.name,
                "role": uo.role.value,
                "joined_at": uo.joined_at.isoformat() if uo.joined_at else None
            })
        
        return members
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error listing members: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{org_id}/members")
async def add_member(
    org_id: UUID,
    member_data: OrganizationMember,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add a member to an organization. Requires admin or owner role.
    """
    try:
        stmt = select(UserOrganization).where(
            and_(
                UserOrganization.organization_id == org_id,
                UserOrganization.user_id == user.id
            )
        )
        result = await db.execute(stmt)
        user_org = result.scalars().first()
        
        if not user_org or user_org.role not in [OrganizationRole.admin, OrganizationRole.owner]:
            raise HTTPException(status_code=403, detail="You don't have permission to add members")
        
        role_enum = OrganizationRole(member_data.role)
        
        existing_stmt = select(UserOrganization).where(
            and_(
                UserOrganization.organization_id == org_id,
                UserOrganization.user_id == UUID(member_data.user_id)
            )
        )
        existing_result = await db.execute(existing_stmt)
        existing = existing_result.scalars().first()
        
        if existing:
            raise HTTPException(status_code=400, detail="User is already a member")
        
        new_member = UserOrganization(
            user_id=UUID(member_data.user_id),
            organization_id=org_id,
            role=role_enum
        )
        db.add(new_member)
        await db.commit()
        
        return {"status": "member_added", "user_id": member_data.user_id}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error adding member: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{org_id}/members/{user_id}")
async def update_member_role(
    org_id: UUID,
    user_id: UUID,
    member_update: OrganizationMemberUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a member's role. Requires admin or owner role.
    """
    try:
        stmt = select(UserOrganization).where(
            and_(
                UserOrganization.organization_id == org_id,
                UserOrganization.user_id == current_user.id
            )
        )
        result = await db.execute(stmt)
        user_org = result.scalars().first()
        
        if not user_org or user_org.role not in [OrganizationRole.admin, OrganizationRole.owner]:
            raise HTTPException(status_code=403, detail="You don't have permission to update roles")
        
        target_stmt = select(UserOrganization).where(
            and_(
                UserOrganization.organization_id == org_id,
                UserOrganization.user_id == user_id
            )
        )
        target_result = await db.execute(target_stmt)
        target_member = target_result.scalars().first()
        
        if not target_member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        role_enum = OrganizationRole(member_update.role)
        target_member.role = role_enum
        await db.commit()
        
        return {"status": "role_updated", "user_id": str(user_id), "new_role": member_update.role}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating member role: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{org_id}/members/{user_id}")
async def remove_member(
    org_id: UUID,
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Remove a member from an organization. Requires admin or owner role.
    """
    try:
        stmt = select(UserOrganization).where(
            and_(
                UserOrganization.organization_id == org_id,
                UserOrganization.user_id == current_user.id
            )
        )
        result = await db.execute(stmt)
        user_org = result.scalars().first()
        
        if not user_org or user_org.role not in [OrganizationRole.admin, OrganizationRole.owner]:
            raise HTTPException(status_code=403, detail="You don't have permission to remove members")
        
        if user_id == current_user.id and user_org.role == OrganizationRole.owner:
            raise HTTPException(status_code=400, detail="Owner cannot remove themselves")
        
        target_stmt = select(UserOrganization).where(
            and_(
                UserOrganization.organization_id == org_id,
                UserOrganization.user_id == user_id
            )
        )
        target_result = await db.execute(target_stmt)
        target_member = target_result.scalars().first()
        
        if not target_member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        await db.delete(target_member)
        await db.commit()
        
        return {"status": "member_removed", "user_id": str(user_id)}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error removing member: {e}")
        raise HTTPException(status_code=500, detail=str(e))

