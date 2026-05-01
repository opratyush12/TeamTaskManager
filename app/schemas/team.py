from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, field_validator
from app.models.team import TeamRole
from app.schemas.user import UserSummary


class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None

    @field_validator('name')
    @classmethod
    def name_validation(cls, v):
        if len(v) < 3:
            raise ValueError('Team name must be at least 3 characters')
        if len(v) > 100:
            raise ValueError('Team name must be less than 100 characters')
        return v


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TeamMemberBase(BaseModel):
    user_id: str
    role: TeamRole = TeamRole.MEMBER


class TeamMemberAdd(BaseModel):
    user_id: str
    role: TeamRole = TeamRole.MEMBER


class TeamMemberUpdate(BaseModel):
    role: TeamRole


class TeamMemberResponse(BaseModel):
    user: UserSummary
    role: TeamRole
    joined_at: datetime

    class Config:
        from_attributes = True


class TeamResponse(TeamBase):
    id: str
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime
    members: Optional[List[TeamMemberResponse]] = None

    class Config:
        from_attributes = True


class TeamSummary(BaseModel):
    id: str
    name: str
    description: Optional[str]
    member_count: Optional[int] = None

    class Config:
        from_attributes = True
