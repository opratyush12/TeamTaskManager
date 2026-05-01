from functools import wraps
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.models.team import TeamMember, TeamRole
from app.database import get_db


def require_role(*allowed_roles: UserRole):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = None, **kwargs):
            if current_user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )

            if current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )

            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator


def check_team_permission(
    db: Session,
    user: User,
    team_id: str,
    required_roles: list[TeamRole] = None
) -> TeamMember:
    if user.role == UserRole.ADMIN:
        membership = db.query(TeamMember).filter(
            TeamMember.team_id == team_id,
            TeamMember.user_id == user.id
        ).first()
        if not membership:
            membership = TeamMember(
                team_id=team_id,
                user_id=user.id,
                role=TeamRole.OWNER
            )
        return membership

    membership = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == user.id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this team"
        )

    if required_roles and membership.role not in required_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient team permissions"
        )

    return membership


def is_team_member(db: Session, user_id: str, team_id: str) -> bool:
    membership = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == user_id
    ).first()
    return membership is not None


def can_manage_team(user: User, team_role: TeamRole) -> bool:
    if user.role == UserRole.ADMIN:
        return True
    return team_role in [TeamRole.OWNER, TeamRole.MANAGER]


def can_delete_team(user: User, team_role: TeamRole) -> bool:
    if user.role == UserRole.ADMIN:
        return True
    return team_role == TeamRole.OWNER
