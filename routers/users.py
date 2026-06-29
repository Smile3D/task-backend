from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.db import get_db
from models.user import User
from pydantic import BaseModel
from auth.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True

# Защищённый эндпоинт — только для авторизованных
@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

@router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.put("/{user_id}")
async def update_user(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    existing_user = result.scalar_one_or_none()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    existing_user.name = user.name
    existing_user.email = user.email
    await db.commit()
    await db.refresh(existing_user)
    return existing_user

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    existing_user = result.scalar_one_or_none()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(existing_user)
    await db.commit()
    return {"message": f"User {user_id} deleted"}