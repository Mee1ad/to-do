from playhouse.migrate import SqliteMigrator, migrate

from db.models.task import *
from schemas.task import *
from settings import DB


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
    space: SpaceSchema = (
        Space
        .select()
        .join(SpaceTaskList, JOIN.LEFT_OUTER)
        .join(TaskList, JOIN.LEFT_OUTER)
        .join(TaskListTask, JOIN.LEFT_OUTER)
        .join(Task, JOIN.LEFT_OUTER)
        .where(Space.id == space_id)
        .first()
    )
    return space


def db_migrate(table: str, field_name: str, field: object) -> None:  # example below
    migrator = SqliteMigrator(DB)
    migrate(
        migrator.add_column(table, field_name, field, )
    )

# example
# user_id_fk = ForeignKeyField(User, backref='spaces', null=False, default='1', field=User.id)
# db_migrate('space', 'user_id', user_id_fk)
