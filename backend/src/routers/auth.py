from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from src.database import get_db
from src.models.user import User
from src.schemas.user import UserCreate, UserLogin, UserResponse, Token
from src.middleware import get_password_hash, verify_password, create_access_token, get_current_user
from src.config import settings

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
async def register(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user"""
    # Check if phone already exists
    result = await db.execute(select(User).where(User.phone == user_create.phone))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )
    
    # Create new user
    db_user = User(
        phone=user_create.phone,
        password_hash=get_password_hash(user_create.password),
        role=user_create.role,
        name=user_create.name,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.post("/login", response_model=Token)
async def login(user_login: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login and get access token"""
    # Find user by phone
    result = await db.execute(select(User).where(User.phone == user_login.phone))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(user_login.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone or password"
        )
    
    if not user.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is disabled"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout (token-based, no server-side logout needed)"""
    return {"message": "Logged out successfully"}
