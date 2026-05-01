from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.team import Team, TeamMember, TeamRole
from app.models.user import User
from app.schemas.team import TeamCreate, TeamUpdate, TeamMemberAdd, TeamMemberUpdate
from app.utils.rbac import check_team_permission, can_manage_team, can_delete_team
from app.services.notification_service import notify_team_invite


def create_team(db: Session, team_data: TeamCreate, creator: User) -> Team:
    existing_team = db.query(Team).filter(Team.name == team_data.name).first()
    if existing_team:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Team name already exists"
        )

    new_team = Team(
        name=team_data.name,
        description=team_data.description,
        created_by=creator.id
    )
    db.add(new_team)
    db.flush()

    creator_membership = TeamMember(
        team_id=new_team.id,
        user_id=creator.id,
        role=TeamRole.OWNER
    )
    db.add(creator_membership)
    db.commit()
    db.refresh(new_team)

    return new_team


def get_user_teams(db: Session, user: User) -> list[Team]:
    memberships = db.query(TeamMember).filter(TeamMember.user_id == user.id).all()
    team_ids = [m.team_id for m in memberships]
    teams = db.query(Team).filter(Team.id.in_(team_ids)).all()
    return teams


def get_team_by_id(db: Session, team_id: str, user: User) -> Team:
    check_team_permission(db, user, team_id)
    team = db.query(Team).filter(Team.id == team_id).first()

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )

    return team


def update_team(db: Session, team_id: str, team_data: TeamUpdate, user: User) -> Team:
    membership = check_team_permission(db, user, team_id)

    if not can_manage_team(user, membership.role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only team owners and managers can update the team"
        )

    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )

    if team_data.name:
        existing = db.query(Team).filter(Team.name == team_data.name, Team.id != team_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Team name already exists"
            )
        team.name = team_data.name

    if team_data.description is not None:
        team.description = team_data.description

    db.commit()
    db.refresh(team)
    return team


def delete_team(db: Session, team_id: str, user: User):
    membership = check_team_permission(db, user, team_id)

    if not can_delete_team(user, membership.role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only team owners can delete the team"
        )

    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )

    db.delete(team)
    db.commit()


def add_team_member(db: Session, team_id: str, member_data: TeamMemberAdd, user: User) -> TeamMember:
    membership = check_team_permission(db, user, team_id)

    if not can_manage_team(user, membership.role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only team owners and managers can add members"
        )

    # Support both user_id and email
    if member_data.email:
        new_member = db.query(User).filter(User.email == member_data.email).first()
        if not new_member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No user found with email: {member_data.email}"
            )
        user_id = new_member.id
    elif member_data.user_id:
        new_member = db.query(User).filter(User.id == member_data.user_id).first()
        if not new_member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        user_id = member_data.user_id
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either user_id or email must be provided"
        )

    existing_membership = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == user_id
    ).first()

    if existing_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a team member"
        )

    new_membership = TeamMember(
        team_id=team_id,
        user_id=user_id,
        role=member_data.role
    )

    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)

    # Send notification
    team = db.query(Team).filter(Team.id == team_id).first()
    if team:
        notify_team_invite(
            db, user_id, team_id,
            team.name, user.full_name
        )

    return new_membership


def remove_team_member(db: Session, team_id: str, user_id: str, current_user: User):
    membership = check_team_permission(db, current_user, team_id)

    if not can_manage_team(current_user, membership.role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only team owners and managers can remove members"
        )

    target_membership = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == user_id
    ).first()

    if not target_membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not a team member"
        )

    if target_membership.role == TeamRole.OWNER:
        owner_count = db.query(TeamMember).filter(
            TeamMember.team_id == team_id,
            TeamMember.role == TeamRole.OWNER
        ).count()

        if owner_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove the last owner"
            )

    db.delete(target_membership)
    db.commit()


def update_member_role(
    db: Session,
    team_id: str,
    user_id: str,
    role_data: TeamMemberUpdate,
    current_user: User
) -> TeamMember:
    membership = check_team_permission(db, current_user, team_id)

    if not can_manage_team(current_user, membership.role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only team owners and managers can update member roles"
        )

    target_membership = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == user_id
    ).first()

    if not target_membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not a team member"
        )

    target_membership.role = role_data.role
    db.commit()
    db.refresh(target_membership)

    return target_membership
