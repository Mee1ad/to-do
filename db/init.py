from settings import DB
from db.models.task import *

task_tables = [Task, TaskList, TaskListTask, Space, SpaceTaskList]


def create_tables():
    with DB:
        DB.create_tables(task_tables)
