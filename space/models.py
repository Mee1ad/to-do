from peewee import AutoField, CharField, IntegerField, ForeignKeyField

from auth.models import User
from settings import BaseModel
from tasklist.models import TaskList


class Space(BaseModel):
    id = AutoField(primary_key=True)
    title = CharField()
    user_id = ForeignKeyField(User, backref='spaces', null=False, on_delete='CASCADE', on_update='CASCADE')
    order = IntegerField(default=99)

    @property
    def space_tasklists(self):
        return SpaceTaskList.select().where(SpaceTaskList.space == self)

    @property
    def tasklists(self):
        tasklists = []
        if self.space_tasklists:
            ordered_space_tasklists = sorted(self.space_tasklists, key=lambda x: x.order)
            for space_tasklist in ordered_space_tasklists:
                tasklist = space_tasklist.tasklist
                if tasklist.archived:
                    continue
                tasklist.space_id = space_tasklist.tasklist_id
                tasklists.append(tasklist)
        return tasklists


class SpaceTaskList(BaseModel):
    space = ForeignKeyField(Space, backref='space_tasklists', on_delete='CASCADE', on_update='CASCADE')
    tasklist = ForeignKeyField(TaskList, backref='space_tasklists', on_delete='CASCADE', on_update='CASCADE')
    order = IntegerField(default=99)

    class Meta:
        table_name = 'space_tasklist'
