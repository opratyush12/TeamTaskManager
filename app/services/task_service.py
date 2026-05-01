from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from app.models.task import Task, TaskStatus, TaskAssignmentStatus
from app.models.project import Project
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskStatusUpdate, TaskAssign
from app.utils.rbac import check_team_permission, is_team_member
from app.services.notification_service import notify_task_assignment, notify_task_completed


def create_task(db: Session, task_data: TaskCreate, creator: User) -> Task:
    project = db.query(Project).filter(Project.id == task_data.project_id).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    check_team_permission(db, creator, project.team_id)

    if task_data.assigned_to:
        if not is_team_member(db, task_data.assigned_to, project.team_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot assign task to user who is not a team member"
            )

    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        project_id=task_data.project_id,
        assigned_to=task_data.assigned_to,
        priority=task_data.priority,
        due_date=task_data.due_date,
        created_by=creator.id,
        assignment_status=TaskAssignmentStatus.PENDING if task_data.assigned_to else None
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # Send notification if task is assigned
    if task_data.assigned_to:
        notify_task_assignment(
            db, task_data.assigned_to, new_task.id,
            new_task.title, creator.full_name
        )

    return new_task


def get_tasks(
    db: Session,
    user: User,
    project_id: str = None,
    status: TaskStatus = None,
    assigned_to: str = None,
    overdue: bool = None,
    sort_by: str = None,
    sort_order: str = "asc"
) -> list[Task]:
    from app.models.team import TeamMember
    from app.models.task import TaskPriority

    memberships = db.query(TeamMember).filter(TeamMember.user_id == user.id).all()
    team_ids = [m.team_id for m in memberships]

    projects = db.query(Project).filter(Project.team_id.in_(team_ids)).all()
    project_ids = [p.id for p in projects]

    query = db.query(Task).filter(Task.project_id.in_(project_ids))

    if project_id:
        query = query.filter(Task.project_id == project_id)

    if status:
        query = query.filter(Task.status == status)

    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)

    if overdue:
        query = query.filter(
            Task.due_date < datetime.utcnow(),
            Task.status != TaskStatus.DONE
        )

    # Sorting
    if sort_by == "priority":
        # Sort by priority: urgent > high > medium > low
        priority_order = {
            TaskPriority.URGENT: 1,
            TaskPriority.HIGH: 2,
            TaskPriority.MEDIUM: 3,
            TaskPriority.LOW: 4
        }
        tasks = query.all()
        tasks.sort(key=lambda t: priority_order.get(t.priority, 5), reverse=(sort_order == "desc"))
        return tasks
    elif sort_by == "due_date":
        if sort_order == "desc":
            query = query.order_by(Task.due_date.desc().nullslast())
        else:
            query = query.order_by(Task.due_date.asc().nullslast())
    elif sort_by == "created_at":
        if sort_order == "desc":
            query = query.order_by(Task.created_at.desc())
        else:
            query = query.order_by(Task.created_at.asc())
    else:
        # Default sort by created_at descending
        query = query.order_by(Task.created_at.desc())

    tasks = query.all()
    return tasks


def get_task_by_id(db: Session, task_id: str, user: User) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    project = db.query(Project).filter(Project.id == task.project_id).first()
    check_team_permission(db, user, project.team_id)

    return task


def update_task(db: Session, task_id: str, task_data: TaskUpdate, user: User) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    project = db.query(Project).filter(Project.id == task.project_id).first()
    membership = check_team_permission(db, user, project.team_id)

    if task.assigned_to != user.id and task.created_by != user.id:
        from app.utils.rbac import can_manage_team
        if not can_manage_team(user, membership.role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update tasks assigned to you or created by you"
            )

    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.status is not None:
        task.status = task_data.status
        if task_data.status == TaskStatus.DONE and not task.completed_at:
            task.completed_at = datetime.utcnow()
        elif task_data.status != TaskStatus.DONE:
            task.completed_at = None
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.assigned_to is not None:
        if not is_team_member(db, task_data.assigned_to, project.team_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot assign task to user who is not a team member"
            )
        task.assigned_to = task_data.assigned_to
    if task_data.due_date is not None:
        task.due_date = task_data.due_date

    db.commit()
    db.refresh(task)

    return task


def update_task_status(db: Session, task_id: str, status_data: TaskStatusUpdate, user: User) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    project = db.query(Project).filter(Project.id == task.project_id).first()
    check_team_permission(db, user, project.team_id)

    task.status = status_data.status

    if status_data.status == TaskStatus.DONE and not task.completed_at:
        task.completed_at = datetime.utcnow()
    elif status_data.status != TaskStatus.DONE:
        task.completed_at = None

    db.commit()
    db.refresh(task)

    return task


def assign_task(db: Session, task_id: str, assign_data: TaskAssign, user: User) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    project = db.query(Project).filter(Project.id == task.project_id).first()
    check_team_permission(db, user, project.team_id)

    if assign_data.assigned_to:
        if not is_team_member(db, assign_data.assigned_to, project.team_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot assign task to user who is not a team member"
            )

    task.assigned_to = assign_data.assigned_to
    task.assignment_status = TaskAssignmentStatus.PENDING if assign_data.assigned_to else None

    db.commit()
    db.refresh(task)

    # Send notification
    if assign_data.assigned_to:
        notify_task_assignment(
            db, assign_data.assigned_to, task.id,
            task.title, user.full_name
        )

    return task


def delete_task(db: Session, task_id: str, user: User):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    project = db.query(Project).filter(Project.id == task.project_id).first()
    membership = check_team_permission(db, user, project.team_id)

    if task.created_by != user.id:
        from app.utils.rbac import can_manage_team
        if not can_manage_team(user, membership.role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only task creator or team managers can delete tasks"
            )

    db.delete(task)
    db.commit()


def accept_task(db: Session, task_id: str, user: User) -> Task:
    """Accept a task assignment"""
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.assigned_to != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only accept tasks assigned to you"
        )

    task.assignment_status = TaskAssignmentStatus.ACCEPTED
    task.status = TaskStatus.IN_PROGRESS

    db.commit()
    db.refresh(task)

    return task


def reject_task(db: Session, task_id: str, user: User) -> Task:
    """Reject a task assignment"""
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.assigned_to != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only reject tasks assigned to you"
        )

    task.assignment_status = TaskAssignmentStatus.REJECTED
    task.assigned_to = None

    db.commit()
    db.refresh(task)

    return task


def complete_task(db: Session, task_id: str, user: User) -> Task:
    """Mark a task as complete"""
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    project = db.query(Project).filter(Project.id == task.project_id).first()
    check_team_permission(db, user, project.team_id)

    # Only assigned user or task creator can mark as complete
    if task.assigned_to and task.assigned_to != user.id and task.created_by != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the assigned user or task creator can mark as complete"
        )

    task.status = TaskStatus.DONE
    task.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(task)

    # Notify task creator if different from completer
    if task.created_by and task.created_by != user.id:
        notify_task_completed(
            db, task.created_by, task.id,
            task.title, user.full_name
        )

    return task
