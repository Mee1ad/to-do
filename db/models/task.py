from peewee import *

db = SqliteDatabase('./db/to-do.sqlite3')


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

    @property
    def task_list_tasks(self):  # prefetched TaskListTask
        return []

    @property
    def tasks(self):
        tasks = []
        if self.task_list_tasks:
            for task_list_tasks in self.task_list_tasks:
                task = task_list_tasks.task
                task.tasklist_id = task_list_tasks.tasklist_id
                tasks.append(task_list_tasks.task)
        return tasks

    class Meta:
        table_name = 'task_list'


class TaskListTask(BaseModel):
    tasklist = ForeignKeyField(TaskList, backref='task_list_tasks')
    task = ForeignKeyField(Task, backref='task_list_tasks')

    class Meta:
        table_name = 'task_list_task'


class Space(BaseModel):
    id = AutoField(primary_key=True)
    title = CharField()

    @property
    def space_task_lists(self):
        return []

    @property
    def task_lists(self):
        task_lists = []
        if self.space_task_lists:
            for space_task_list in self.space_task_lists:
                task_list = space_task_list.task_list
                task_list.space_id = space_task_list.task_list_id
                task_lists.append(task_list)
        return task_lists


class SpaceTaskList(BaseModel):
    space = ForeignKeyField(Space, backref='space_task_lists')
    task_list = ForeignKeyField(TaskList, backref='space_task_lists')

    class Meta:
        table_name = 'space_task_list'
