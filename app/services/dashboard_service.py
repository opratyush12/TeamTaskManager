from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.project import Project
from app.models.team import TeamMember
from app.models.user import User


def get_dashboard_overview(db: Session, user: User) -> dict:
    memberships = db.query(TeamMember).filter(TeamMember.user_id == user.id).all()
    team_ids = [m.team_id for m in memberships]

    projects = db.query(Project).filter(Project.team_id.in_(team_ids)).all()
    project_ids = [p.id for p in projects]

    total_tasks = db.query(Task).filter(Task.project_id.in_(project_ids)).count()

    tasks_by_status = db.query(
        Task.status,
        func.count(Task.id).label('count')
    ).filter(
        Task.project_id.in_(project_ids)
    ).group_by(Task.status).all()

    status_counts = [{"status": str(status.value), "count": count} for status, count in tasks_by_status]

    now = datetime.utcnow()
    today_end = now.replace(hour=23, minute=59, second=59)
    week_end = now + timedelta(days=7)

    overdue_tasks = db.query(Task).filter(
        Task.project_id.in_(project_ids),
        Task.due_date < now,
        Task.status != TaskStatus.DONE
    ).count()

    tasks_due_today = db.query(Task).filter(
        Task.project_id.in_(project_ids),
        Task.due_date <= today_end,
        Task.due_date >= now,
        Task.status != TaskStatus.DONE
    ).count()

    tasks_due_this_week = db.query(Task).filter(
        Task.project_id.in_(project_ids),
        Task.due_date <= week_end,
        Task.due_date >= now,
        Task.status != TaskStatus.DONE
    ).count()

    my_tasks = db.query(Task).filter(
        Task.project_id.in_(project_ids),
        Task.assigned_to == user.id,
        Task.status != TaskStatus.DONE
    ).count()

    return {
        "total_tasks": total_tasks,
        "tasks_by_status": status_counts,
        "overdue_tasks": overdue_tasks,
        "tasks_due_today": tasks_due_today,
        "tasks_due_this_week": tasks_due_this_week,
        "my_tasks": my_tasks
    }


def get_dashboard_tasks(db: Session, user: User) -> dict:
    memberships = db.query(TeamMember).filter(TeamMember.user_id == user.id).all()
    team_ids = [m.team_id for m in memberships]

    projects = db.query(Project).filter(Project.team_id.in_(team_ids)).all()
    project_ids = [p.id for p in projects]

    my_tasks = db.query(Task).filter(
        Task.project_id.in_(project_ids),
        Task.assigned_to == user.id,
        Task.status != TaskStatus.DONE
    ).order_by(Task.due_date.asc()).limit(10).all()

    team_tasks = db.query(Task).filter(
        Task.project_id.in_(project_ids),
        Task.status != TaskStatus.DONE
    ).order_by(Task.created_at.desc()).limit(10).all()

    now = datetime.utcnow()
    overdue_tasks = db.query(Task).filter(
        Task.project_id.in_(project_ids),
        Task.due_date < now,
        Task.status != TaskStatus.DONE
    ).order_by(Task.due_date.asc()).limit(10).all()

    return {
        "my_tasks": my_tasks,
        "team_tasks": team_tasks,
        "overdue_tasks": overdue_tasks
    }


def get_dashboard_stats(db: Session, user: User) -> dict:
    memberships = db.query(TeamMember).filter(TeamMember.user_id == user.id).all()
    team_ids = [m.team_id for m in memberships]

    projects = db.query(Project).filter(Project.team_id.in_(team_ids)).all()
    project_ids = [p.id for p in projects]

    tasks_by_priority = db.query(
        Task.priority,
        func.count(Task.id).label('count')
    ).filter(
        Task.project_id.in_(project_ids)
    ).group_by(Task.priority).all()

    priority_counts = [{"priority": str(priority.value), "count": count} for priority, count in tasks_by_priority]

    total_tasks = db.query(Task).filter(Task.project_id.in_(project_ids)).count()
    completed_tasks = db.query(Task).filter(
        Task.project_id.in_(project_ids),
        Task.status == TaskStatus.DONE
    ).count()

    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0

    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    tasks_completed_last_7_days = db.query(Task).filter(
        Task.project_id.in_(project_ids),
        Task.status == TaskStatus.DONE,
        Task.completed_at >= seven_days_ago
    ).count()

    tasks_created_last_7_days = db.query(Task).filter(
        Task.project_id.in_(project_ids),
        Task.created_at >= seven_days_ago
    ).count()

    return {
        "tasks_by_priority": priority_counts,
        "completion_rate": round(completion_rate, 2),
        "tasks_completed_last_7_days": tasks_completed_last_7_days,
        "tasks_created_last_7_days": tasks_created_last_7_days
    }
