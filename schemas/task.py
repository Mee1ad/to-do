from dataclasses import dataclass


@dataclass
class TaskSchema:
    id: int
    title: str
    checked: str


@dataclass
class TaskListSchema:
    id: int
    title: str
    tasks: list[TaskSchema]


@dataclass
class SpaceSchema:
    id: int
    title: str
    task_lists: list[TaskListSchema]
