import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class NotificationType(str, enum.Enum):
    TASK_ASSIGNED = "task_assigned"
    TASK_COMPLETED = "task_completed"
    TASK_UPDATED = "task_updated"
    TEAM_INVITE = "team_invite"
    TEAM_REMOVED = "team_removed"
    PROJECT_CREATED = "project_created"
    DEADLINE_APPROACHING = "deadline_approaching"
    TASK_OVERDUE = "task_overdue"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    link = Column(String(500), nullable=True)  # Link to related resource
    is_read = Column(Boolean, default=False)
    data = Column(Text, nullable=True)  # JSON string for additional data
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="notifications")
