from peewee import AutoField, CharField, IntegerField, ForeignKeyField

from auth.models import User
from settings import BaseModel
from task.models import Task


class TaskList(BaseModel):
    id = AutoField(primary_key=True)
    title = CharField()
    user_id = ForeignKeyField(User, backref='tasklists', null=False, on_delete='CASCADE', on_update='CASCADE')

    @property
    def tasklist_tasks(self):  # prefetched TaskListTask
        return TaskListTask.select().where(TaskListTask.tasklist == self)

    @property
    def tasks(self):
        tasks = []
        if self.tasklist_tasks:
            ordered_tasklist_tasks = sorted(self.tasklist_tasks, key=lambda x: x.order)
            for tasklist_tasks in ordered_tasklist_tasks:
                task = tasklist_tasks.task
                task.tasklist_id = tasklist_tasks.tasklist_id
                tasks.append(tasklist_tasks.task)
        return tasks

    class Meta:
        table_name = 'tasklist'


class TaskListTask(BaseModel):
    tasklist = ForeignKeyField(TaskList, backref='tasklist_tasks', on_delete='CASCADE', on_update='CASCADE')
    task = ForeignKeyField(Task, backref='tasklist_tasks', on_delete='CASCADE', on_update='CASCADE')
    order = IntegerField(default=99)

    class Meta:
        table_name = 'tasklist_task'
