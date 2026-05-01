from pydantic import BaseModel
from typing import Dict, List
from app.schemas.task import TaskSummary


class TaskStatusCount(BaseModel):
    status: str
    count: int


class DashboardOverview(BaseModel):
    total_tasks: int
    tasks_by_status: List[TaskStatusCount]
    overdue_tasks: int
    tasks_due_today: int
    tasks_due_this_week: int
    my_tasks: int


class DashboardTasks(BaseModel):
    my_tasks: List[TaskSummary]
    team_tasks: List[TaskSummary]
    overdue_tasks: List[TaskSummary]


class PriorityCount(BaseModel):
    priority: str
    count: int


class DashboardStats(BaseModel):
    tasks_by_priority: List[PriorityCount]
    completion_rate: float
    tasks_completed_last_7_days: int
    tasks_created_last_7_days: int
