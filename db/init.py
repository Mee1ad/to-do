from db.models.auth import *
from db.models.task import *

task_tables = [Task, TaskList, TaskListTask, Space, SpaceTaskList]
auth_tables = [User, Login]


def create_tables():
    with DB:
        DB.create_tables(task_tables)
        DB.create_tables(auth_tables)
