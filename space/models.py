from peewee import AutoField, CharField, IntegerField, ForeignKeyField

from auth.models import User
from settings import BaseModel
from tasklist.models import TaskList


class Space(BaseModel):
    id = AutoField(primary_key=True)
    title = CharField()
    user_id = ForeignKeyField(User, backref='spaces', null=False, on_delete='CASCADE', on_update='CASCADE')

    @property
    def space_tasklists(self):
        return SpaceTaskList.select().where(SpaceTaskList.space == self)

    @property
    def tasklists(self):
        tasklists = []
        if self.space_tasklists:
            for space_tasklist in self.space_tasklists:
                tasklist = space_tasklist.tasklist
                tasklist.space_id = space_tasklist.tasklist_id
                tasklists.append(tasklist)
        return tasklists


class SpaceTaskList(BaseModel):
    space = ForeignKeyField(Space, backref='space_tasklists', on_delete='CASCADE', on_update='CASCADE')
    tasklist = ForeignKeyField(TaskList, backref='space_tasklists', on_delete='CASCADE', on_update='CASCADE')
    order = IntegerField()

    class Meta:
        table_name = 'space_tasklist'
