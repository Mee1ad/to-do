from peewee import *

from db.models.auth import User

db = SqliteDatabase('./db/to-do.sqlite3', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db


class Task(BaseModel):
    id = AutoField(primary_key=True)
    title = CharField()
    checked = BooleanField(default=False)


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


class Space(BaseModel):
    id = AutoField(primary_key=True)
    title = CharField()
    user_id = ForeignKeyField(User, backref='spaces', null=False, on_delete='CASCADE', on_update='CASCADE')

    @property
    def space_tasklists(self):
        return []

    @property
    def tasklists(self):
        tasklists = []
        print('self.space_tasklists', self.space_tasklists)
        if self.space_tasklists:
            for space_tasklist in self.space_tasklists:
                tasklist = space_tasklist.tasklist
                tasklist.space_id = space_tasklist.tasklist_id
                tasklists.append(tasklist)
        return tasklists


class SpaceTaskList(BaseModel):
    space = ForeignKeyField(Space, backref='space_tasklists', on_delete='CASCADE', on_update='CASCADE')
    tasklist = ForeignKeyField(TaskList, backref='space_tasklists', on_delete='CASCADE', on_update='CASCADE')

    class Meta:
        table_name = 'space_tasklist'
