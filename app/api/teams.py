from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.team import (
    TeamCreate,
    TeamUpdate,
    TeamResponse,
    TeamMemberAdd,
    TeamMemberUpdate,
    TeamMemberResponse
)
from app.services.team_service import (
    create_team,
    get_user_teams,
    get_team_by_id,
    update_team,
    delete_team,
    add_team_member,
    remove_team_member,
    update_member_role
)

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_new_team(
    team_data: TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_team(db, team_data, current_user)


@router.get("", response_model=List[TeamResponse])
def list_teams(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_teams(db, current_user)


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_team_by_id(db, team_id, current_user)


@router.put("/{team_id}", response_model=TeamResponse)
def update_team_info(
    team_id: str,
    team_data: TeamUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_team(db, team_id, team_data, current_user)


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team_by_id(
    team_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delete_team(db, team_id, current_user)


@router.post("/{team_id}/members", response_model=TeamMemberResponse, status_code=status.HTTP_201_CREATED)
def add_member(
    team_id: str,
    member_data: TeamMemberAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return add_team_member(db, team_id, member_data, current_user)


@router.delete("/{team_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member(
    team_id: str,
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    remove_team_member(db, team_id, user_id, current_user)


@router.put("/{team_id}/members/{user_id}/role", response_model=TeamMemberResponse)
def update_member_role_endpoint(
    team_id: str,
    user_id: str,
    role_data: TeamMemberUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_member_role(db, team_id, user_id, role_data, current_user)
