from db.models.auth import User, Login
from db.models.task import Space, TaskList, TaskListTask, Task


def clear_session(session: dict):
    user_id = session.get("user_id", None)
    tasks = Task.select().join(TaskListTask).join(TaskList).where(TaskList.user_id == user_id)
    Task.delete().where(Task.id.in_(tasks)).execute()
    TaskList.delete().where(TaskList.user_id == user_id).execute()
    Space.delete().where(Space.user_id == user_id).execute()
    Login.delete().where(Login.user == user_id, Login.provider == 'session').execute()
    User.delete().where(User.id == user_id).execute()
