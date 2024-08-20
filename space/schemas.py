from pydantic import BaseModel, constr

from tasklist.schemas import TaskListSchema


class SpaceSchema(BaseModel):
    id: int
    title: str
    tasklists: list[TaskListSchema]


class SpaceCreateSchema(BaseModel):
    title: constr(min_length=1)
