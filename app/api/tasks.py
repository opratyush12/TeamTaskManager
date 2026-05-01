from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.task import TaskStatus
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskStatusUpdate,
    TaskAssign
)
from app.services.task_service import (
    create_task,
    get_tasks,
    get_task_by_id,
    update_task,
    update_task_status,
    assign_task,
    delete_task
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_task(db, task_data, current_user)


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    project_id: Optional[str] = Query(None),
    status: Optional[TaskStatus] = Query(None),
    assigned_to: Optional[str] = Query(None),
    overdue: Optional[bool] = Query(None),
    sort_by: Optional[str] = Query(None, description="Sort by: priority, due_date, created_at"),
    sort_order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_tasks(db, current_user, project_id, status, assigned_to, overdue, sort_by, sort_order)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_task_by_id(db, task_id, current_user)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task_info(
    task_id: str,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_task(db, task_id, task_data, current_user)


@router.put("/{task_id}/status", response_model=TaskResponse)
def update_status(
    task_id: str,
    status_data: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_task_status(db, task_id, status_data, current_user)


@router.put("/{task_id}/assign", response_model=TaskResponse)
def assign_task_to_user(
    task_id: str,
    assign_data: TaskAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return assign_task(db, task_id, assign_data, current_user)


@router.put("/{task_id}/accept", response_model=TaskResponse)
def accept_task_assignment(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.services.task_service import accept_task
    return accept_task(db, task_id, current_user)


@router.put("/{task_id}/reject", response_model=TaskResponse)
def reject_task_assignment(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.services.task_service import reject_task
    return reject_task(db, task_id, current_user)


@router.put("/{task_id}/complete", response_model=TaskResponse)
def mark_task_complete(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.services.task_service import complete_task
    return complete_task(db, task_id, current_user)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_by_id(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delete_task(db, task_id, current_user)
