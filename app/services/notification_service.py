from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.notification import Notification, NotificationType
from app.models.user import User
from app.schemas.notification import NotificationCreate
import json


def create_notification(db: Session, notification_data: NotificationCreate) -> Notification:
    """Create a new notification for a user"""
    notification = Notification(
        user_id=notification_data.user_id,
        type=notification_data.type,
        title=notification_data.title,
        message=notification_data.message,
        link=notification_data.link,
        data=notification_data.data
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def get_user_notifications(db: Session, user: User, unread_only: bool = False) -> list[Notification]:
    """Get all notifications for a user"""
    query = db.query(Notification).filter(Notification.user_id == user.id)

    if unread_only:
        query = query.filter(Notification.is_read == False)

    return query.order_by(Notification.created_at.desc()).all()


def mark_notifications_read(db: Session, notification_ids: list[str], user: User):
    """Mark notifications as read"""
    notifications = db.query(Notification).filter(
        Notification.id.in_(notification_ids),
        Notification.user_id == user.id
    ).all()

    for notification in notifications:
        notification.is_read = True

    db.commit()


def mark_all_read(db: Session, user: User):
    """Mark all user notifications as read"""
    db.query(Notification).filter(
        Notification.user_id == user.id,
        Notification.is_read == False
    ).update({"is_read": True})
    db.commit()


def delete_notification(db: Session, notification_id: str, user: User):
    """Delete a notification"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user.id
    ).first()

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    db.delete(notification)
    db.commit()


def get_unread_count(db: Session, user: User) -> int:
    """Get count of unread notifications"""
    return db.query(Notification).filter(
        Notification.user_id == user.id,
        Notification.is_read == False
    ).count()


# Helper functions to create specific notification types
def notify_task_assignment(db: Session, user_id: str, task_id: str, task_title: str, assigner_name: str):
    """Notify user about task assignment"""
    notification_data = NotificationCreate(
        user_id=user_id,
        type=NotificationType.TASK_ASSIGNED,
        title="New Task Assigned",
        message=f"{assigner_name} assigned you a task: {task_title}",
        link=f"/tasks/{task_id}",
        data=json.dumps({"task_id": task_id, "assigner": assigner_name})
    )
    return create_notification(db, notification_data)


def notify_team_invite(db: Session, user_id: str, team_id: str, team_name: str, inviter_name: str):
    """Notify user about team invitation"""
    notification_data = NotificationCreate(
        user_id=user_id,
        type=NotificationType.TEAM_INVITE,
        title="Team Invitation",
        message=f"{inviter_name} added you to team: {team_name}",
        link=f"/teams/{team_id}",
        data=json.dumps({"team_id": team_id, "inviter": inviter_name})
    )
    return create_notification(db, notification_data)


def notify_task_completed(db: Session, user_id: str, task_id: str, task_title: str, completer_name: str):
    """Notify user about task completion"""
    notification_data = NotificationCreate(
        user_id=user_id,
        type=NotificationType.TASK_COMPLETED,
        title="Task Completed",
        message=f"{completer_name} completed: {task_title}",
        link=f"/tasks/{task_id}",
        data=json.dumps({"task_id": task_id, "completer": completer_name})
    )
    return create_notification(db, notification_data)


def notify_deadline_approaching(db: Session, user_id: str, task_id: str, task_title: str, hours_remaining: int):
    """Notify user about approaching deadline"""
    notification_data = NotificationCreate(
        user_id=user_id,
        type=NotificationType.DEADLINE_APPROACHING,
        title="Deadline Approaching",
        message=f"Task '{task_title}' is due in {hours_remaining} hours",
        link=f"/tasks/{task_id}",
        data=json.dumps({"task_id": task_id, "hours_remaining": hours_remaining})
    )
    return create_notification(db, notification_data)


def notify_task_overdue(db: Session, user_id: str, task_id: str, task_title: str):
    """Notify user about overdue task"""
    notification_data = NotificationCreate(
        user_id=user_id,
        type=NotificationType.TASK_OVERDUE,
        title="Task Overdue",
        message=f"Task '{task_title}' is now overdue",
        link=f"/tasks/{task_id}",
        data=json.dumps({"task_id": task_id})
    )
    return create_notification(db, notification_data)
