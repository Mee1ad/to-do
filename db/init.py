from auth.models import User, Login
from settings import DB
from space.models import Space, SpaceTaskList
from task.models import Task
from tasklist.models import TaskList, TaskListTask

task_tables = [Task, TaskList, TaskListTask, Space, SpaceTaskList]
auth_tables = [User, Login]


def create_tables():
    with DB:
        DB.create_tables(task_tables)
        DB.create_tables(auth_tables)
