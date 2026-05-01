from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.notification import NotificationType


class NotificationBase(BaseModel):
    title: str
    message: str
    type: NotificationType
    link: Optional[str] = None


class NotificationCreate(NotificationBase):
    user_id: str
    data: Optional[str] = None


class NotificationResponse(NotificationBase):
    id: str
    is_read: bool
    created_at: datetime
    data: Optional[str] = None

    class Config:
        from_attributes = True


class NotificationMarkRead(BaseModel):
    notification_ids: list[str]
