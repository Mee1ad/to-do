from peewee import prefetch
from playhouse.migrate import SqliteMigrator, migrate

from settings import DB
from space.models import Space, SpaceTaskList
from task.models import Task
from tasklist.models import TaskList, TaskListTask


def get_tasklist_by_id(tasklist_id: int):
    return (
        TaskList
        .select()
        .join(TaskListTask)
        .join(Task)
        .where(TaskList.id == tasklist_id)
        .first()
    )


def get_space_by_id(space_id: int):
    space_query = (
        Space
        .select()
        .where(Space.id == space_id)
    )

    ordered_space_tasklists_query = (
        SpaceTaskList
        .select()
        .where(SpaceTaskList.space == space_id)
        .order_by(SpaceTaskList.order)
    )

    ordered_tasklist_tasks_query = (
        TaskListTask
        .select()
        .where(TaskListTask.tasklist << ordered_space_tasklists_query)
        .order_by(TaskListTask.order)
    )

    return prefetch(space_query, ordered_space_tasklists_query, TaskList, ordered_tasklist_tasks_query, Task)[0]


def db_migrate(table: str, field_name: str, field: object) -> None:  # example below
    migrator = SqliteMigrator(DB)
    migrate(
        migrator.add_column(table, field_name, field, )
    )

# example
# user_id_fk = ForeignKeyField(User, backref='spaces', null=False, default='1', field=User.id)
# db_migrate('space', 'user_id', user_id_fk)
