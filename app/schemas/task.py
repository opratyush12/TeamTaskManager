from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator
from app.models.task import TaskStatus, TaskPriority
from app.schemas.user import UserSummary


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None

    @field_validator('title')
    @classmethod
    def title_validation(cls, v):
        if len(v) < 3:
            raise ValueError('Task title must be at least 3 characters')
        if len(v) > 200:
            raise ValueError('Task title must be less than 200 characters')
        return v

    @field_validator('due_date')
    @classmethod
    def due_date_validation(cls, v):
        if v and v < datetime.utcnow():
            raise ValueError('Due date cannot be in the past')
        return v


class TaskCreate(TaskBase):
    project_id: str
    assigned_to: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskAssign(BaseModel):
    assigned_to: Optional[str] = None


class TaskResponse(TaskBase):
    id: str
    project_id: str
    status: TaskStatus
    assigned_to: Optional[str]
    created_by: Optional[str]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    assignee: Optional[UserSummary] = None
    creator: Optional[UserSummary] = None

    class Config:
        from_attributes = True


class TaskSummary(BaseModel):
    id: str
    title: str
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime]
    project_id: str

    class Config:
        from_attributes = True
