from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.project import Project
from app.models.team import TeamRole
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.utils.rbac import check_team_permission, can_manage_team


def create_project(db: Session, project_data: ProjectCreate, creator: User) -> Project:
    membership = check_team_permission(db, creator, project_data.team_id)

    if not can_manage_team(creator, membership.role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only team owners and managers can create projects"
        )

    new_project = Project(
        name=project_data.name,
        description=project_data.description,
        team_id=project_data.team_id,
        start_date=project_data.start_date,
        end_date=project_data.end_date,
        created_by=creator.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


def get_projects(db: Session, user: User, team_id: str = None) -> list[Project]:
    if team_id:
        check_team_permission(db, user, team_id)
        projects = db.query(Project).filter(Project.team_id == team_id).all()
    else:
        from app.models.team import TeamMember
        memberships = db.query(TeamMember).filter(TeamMember.user_id == user.id).all()
        team_ids = [m.team_id for m in memberships]
        projects = db.query(Project).filter(Project.team_id.in_(team_ids)).all()

    return projects


def get_project_by_id(db: Session, project_id: str, user: User) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    check_team_permission(db, user, project.team_id)

    return project


def update_project(db: Session, project_id: str, project_data: ProjectUpdate, user: User) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    membership = check_team_permission(db, user, project.team_id)

    if not can_manage_team(user, membership.role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only team owners and managers can update projects"
        )

    if project_data.name is not None:
        project.name = project_data.name
    if project_data.description is not None:
        project.description = project_data.description
    if project_data.status is not None:
        project.status = project_data.status
    if project_data.start_date is not None:
        project.start_date = project_data.start_date
    if project_data.end_date is not None:
        project.end_date = project_data.end_date

    db.commit()
    db.refresh(project)

    return project


def delete_project(db: Session, project_id: str, user: User):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    membership = check_team_permission(db, user, project.team_id)

    if not can_manage_team(user, membership.role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only team owners and managers can delete projects"
        )

    db.delete(project)
    db.commit()
