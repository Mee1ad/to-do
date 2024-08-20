from peewee import AutoField, CharField, ForeignKeyField

from auth.models import User
from settings import BaseModel
from task.models import Task


class TaskList(BaseModel):
    id = AutoField(primary_key=True)
    title = CharField()
    user_id = ForeignKeyField(User, backref='tasklists', null=False, on_delete='CASCADE', on_update='CASCADE')

    @property
    def tasklist_tasks(self):  # prefetched TaskListTask
        return []

    @property
    def tasks(self):
        tasks = []
        if self.tasklist_tasks:
            for tasklist_tasks in self.tasklist_tasks:
                task = tasklist_tasks.task
                task.tasklist_id = tasklist_tasks.tasklist_id
                tasks.append(tasklist_tasks.task)
        return tasks

    class Meta:
        table_name = 'tasklist'


class TaskListTask(BaseModel):
    tasklist = ForeignKeyField(TaskList, backref='tasklist_tasks', on_delete='CASCADE', on_update='CASCADE')
    task = ForeignKeyField(Task, backref='tasklist_tasks', on_delete='CASCADE', on_update='CASCADE')

    class Meta:
        table_name = 'tasklist_task'
