from django.utils.timezone import now
from .models import Task

def get_due_today_notifications(user):
    today = now().date()
    # Use 'assignee' instead of 'user' to filter tasks
    tasks_due_today = Task.objects.filter(assignee=user, due_date=today)
    notifications = []
    for task in tasks_due_today:
        notifications.append({
            'task_id': task.unique_id,
            'title': task.title,
            'status': task.status,
            'priority': task.priority,
            'due_date': task.due_date,
        })
    return notifications