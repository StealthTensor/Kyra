from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models import User, Account
from app.core.config import settings
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
import os

router = APIRouter()

# Scopes verified against rules-email.md (ReadOnly for now)
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly'
]

def get_flow(request: Request):
    redirect_uri = f"{settings.API_BASE_URL}{settings.API_V1_STR}/auth/callback"
    
    client_config = {
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [redirect_uri]
        }
    }
    
    flow = Flow.from_client_config(
        client_config=client_config,
        scopes=SCOPES
    )
    flow.redirect_uri = redirect_uri
    return flow

@router.get("/login")
async def login(request: Request):
    flow = get_flow(request)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    # Ideally store state in session to verify in callback
    return RedirectResponse(authorization_url)

@router.get("/callback")
async def callback(request: Request, code: str, state: str = None, db: AsyncSession = Depends(get_db)):
    try:
        flow = get_flow(request)
        flow.fetch_token(code=code)
        
        creds = flow.credentials
        
        # Get User Info
        service = build('oauth2', 'v2', credentials=creds)
        user_info = service.userinfo().get().execute()
        
        email = user_info.get('email')
        name = user_info.get('name')
        picture = user_info.get('picture')
        google_id = user_info.get('id')
        
        if not email:
            raise HTTPException(status_code=400, detail="Could not retrieve email from Google")

        # Database Ops
        # 1. UPSERT User
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        user = result.scalars().first()
        
        if not user:
            user = User(
                email=email,
                name=name,
                avatar=picture,
                # is_active=True default
            )
            db.add(user)
            await db.flush() # get ID
            
        else:
            # Update fields if changed
            user.name = name
            user.avatar = picture
            
        # 2. UPSERT Account (Tokens)
        stmt = select(Account).where(Account.user_id == user.id)
        result = await db.execute(stmt)
        account = result.scalars().first()
        
        if not account:
            account = Account(
                user_id=user.id,
                email_address=email,
                access_token=creds.token,
                refresh_token=creds.refresh_token,
                token_expiry=creds.expiry
            )
            db.add(account)
        else:
            account.access_token = creds.token
            if creds.refresh_token:
                account.refresh_token = creds.refresh_token
            account.token_expiry = creds.expiry
            
        await db.commit()
        await db.refresh(user)
        
        # Redirect to Frontend with simplistic token passing
        # For MVP: encoding user data in query params. 
        # In Prod: Use Session Cookie or dedicated JWT.
        
        import base64
        # Create a simple "token" which is just userId for this MVP (User rules said "Broke but Pro" but we need speed)
        # Or better, just pass the raw data so frontend store updates.
        
        # We will redirect to /auth/callback on frontend which doesn't exist yet, 
        # Or reuse /login with params.
        
        from app.core.config import settings
        frontend_url = f"{settings.FRONTEND_URL}/auth/login"
        
        # Generate JWT token
        from app.core.auth import create_access_token
        
        access_token = create_access_token(data={"sub": str(user.id)})
        
        # Safe URL encoding
        from urllib.parse import urlencode
        
        params = {
            "token": access_token,
            "user_id": str(user.id),
            "email": email,
            "name": name,
            "avatar": picture,
            "callback_success": "true"
        }
        
        redirect_url = f"{frontend_url}?{urlencode(params)}"
        return RedirectResponse(redirect_url)
        
    except Exception as e:
        print(f"Auth Error: {e}")
        from app.core.config import settings
        return RedirectResponse(f"{settings.FRONTEND_URL}/auth/login?error=auth_failed")
