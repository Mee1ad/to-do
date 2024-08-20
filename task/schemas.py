from pydantic import BaseModel, constr


class TaskSchema(BaseModel):
    id: int
    title: str
    checked: str


class TaskCreateSchema(BaseModel):
    task_text: constr(min_length=1)
    tasklist_id: int
