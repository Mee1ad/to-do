from dataclasses import dataclass
from pydantic import BaseModel, StrictStr, StrictInt, constr


class TaskListSchema(BaseModel):
    id: int
    title: str
    tasks: list['TaskSchema']  # Forward reference to TaskSchema


class TaskListCreateSchema(BaseModel):
    task_list_title: constr(min_length=1)
    space_id: int


class TaskListUpdateSchema(BaseModel):
    id: int
    title: constr(min_length=1)


class TaskSchema(BaseModel):
    id: int
    title: str
    checked: str
    task_list_id: TaskListSchema


class TaskCreateSchema(BaseModel):
    task_text: constr(min_length=1)
    tasklist_id: int


class SpaceSchema(BaseModel):
    id: int
    title: str
    task_lists: list[TaskListSchema]


class SpaceCreateSchema(BaseModel):
    title: constr(min_length=1)
