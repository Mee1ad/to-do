from pydantic import BaseModel, constr


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


class TaskSchema(BaseModel):
    id: int
    title: str
    checked: str
    tasklist_id: TaskListSchema


class TaskCreateSchema(BaseModel):
    task_text: constr(min_length=1)
    tasklist_id: int


class SpaceSchema(BaseModel):
    id: int
    title: str
    tasklists: list[TaskListSchema]


class SpaceCreateSchema(BaseModel):
    title: constr(min_length=1)
