from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.db import get_db
from models.task import Task
from models.user import User
from auth.dependencies import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/tasks", tags=["tasks"])

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = "todo"

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    user_id: int

    class Config:
        from_attributes = True

# Получить все задачи текущего юзера
@router.get("/", response_model=list[TaskResponse])
async def get_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Task).where(Task.user_id == current_user.id)
    )
    return result.scalars().all()

# Создать задачу
@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=current_user.id
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

# Обновить статус задачи
@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    existing_task = result.scalar_one_or_none()

    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    existing_task.title = task.title
    existing_task.description = task.description
    existing_task.status = task.status
    await db.commit()
    await db.refresh(existing_task)
    return existing_task

# Удалить задачу
@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    existing_task = result.scalar_one_or_none()

    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(existing_task)
    await db.commit()
    return {"message": f"Task {task_id} deleted"}