from dataclasses import dataclass
from pydantic import BaseModel, StrictStr, StrictInt, constr


class TaskListSchema(BaseModel):
    id: int
    title: str
    tasks: list['TaskSchema']  # Forward reference to TaskSchema


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
