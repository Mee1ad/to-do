from pydantic import BaseModel, constr

from task.schemas import TaskSchema


class TaskListSchema(BaseModel):
    id: int
    title: str
    tasks: list['TaskSchema']  # Forward reference to TaskSchema


class TaskListCreateSchema(BaseModel):
    tasklist_title: constr(min_length=1)
    space_id: int


class TaskListUpdateSchema(BaseModel):
    id: int
    title: constr(min_length=1)
