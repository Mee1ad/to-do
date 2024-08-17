from settings import db
from db.models.task import *

task_tables = [Task, TaskList, TaskListTask, Space, SpaceTaskList]


def create_tables():
    with db:
        db.create_tables(task_tables)
