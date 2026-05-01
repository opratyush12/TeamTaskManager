from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, field_validator
from app.models.project import ProjectStatus


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    @field_validator('name')
    @classmethod
    def name_validation(cls, v):
        if len(v) < 3:
            raise ValueError('Project name must be at least 3 characters')
        if len(v) > 200:
            raise ValueError('Project name must be less than 200 characters')
        return v

    @field_validator('end_date')
    @classmethod
    def end_date_validation(cls, v, info):
        if v and 'start_date' in info.data and info.data['start_date']:
            if v < info.data['start_date']:
                raise ValueError('End date must be after start date')
        return v


class ProjectCreate(ProjectBase):
    team_id: str


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ProjectResponse(ProjectBase):
    id: str
    team_id: str
    status: ProjectStatus
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime
    task_count: Optional[int] = None

    class Config:
        from_attributes = True


class ProjectSummary(BaseModel):
    id: str
    name: str
    status: ProjectStatus
    team_id: str

    class Config:
        from_attributes = True
