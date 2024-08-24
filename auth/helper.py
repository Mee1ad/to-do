from workos import WorkOSClient

from auth.models import User, Login
from auth.schemas import UserSchema
from settings import env
from space.models import Space
from task.models import Task
from tasklist.models import TaskList, TaskListTask

workos_client = WorkOSClient(api_key=env.workos_api_key, client_id=env.workos_client_id)


def get_login_url() -> str:
    provider = "GoogleOAuth"
    redirect_uri = f"{env.domain}/auth/callback"
    authorization_url = workos_client.sso.get_authorization_url(
        provider="GoogleOAuth", redirect_uri=redirect_uri
    )

    return authorization_url


def get_user_from_session(session) -> UserSchema | None:
    if session.get("user_id", None):
        print('dddddddddddddddddddddddd', session.get("user_id", None))
        return User.get(id=session["user_id"])
    return None


def clear_session(session: dict):
    user_id = session.get("user_id", None)
    tasks = Task.select().join(TaskListTask).join(TaskList).where(TaskList.user_id == user_id)
    Task.delete().where(Task.id.in_(tasks)).execute()
    TaskList.delete().where(TaskList.user_id == user_id).execute()
    Space.delete().where(Space.user_id == user_id).execute()
    Login.delete().where(Login.user == user_id, Login.provider == 'session').execute()
    User.delete().where(User.id == user_id).execute()
