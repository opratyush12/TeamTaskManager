from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.notification import NotificationResponse, NotificationMarkRead
from app.services.notification_service import (
    get_user_notifications,
    mark_notifications_read,
    mark_all_read,
    delete_notification,
    get_unread_count
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=List[NotificationResponse])
def list_notifications(
    unread_only: bool = Query(False, description="Filter to show only unread notifications"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all notifications for the current user"""
    return get_user_notifications(db, current_user, unread_only)


@router.get("/unread-count", response_model=dict)
def get_unread_notifications_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get count of unread notifications"""
    count = get_unread_count(db, current_user)
    return {"unread_count": count}


@router.put("/mark-read", status_code=status.HTTP_204_NO_CONTENT)
def mark_read(
    notification_data: NotificationMarkRead,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark specific notifications as read"""
    mark_notifications_read(db, notification_data.notification_ids, current_user)


@router.put("/mark-all-read", status_code=status.HTTP_204_NO_CONTENT)
def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark all notifications as read"""
    mark_all_read(db, current_user)


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification_by_id(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a notification"""
    delete_notification(db, notification_id, current_user)
