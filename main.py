from components.task_components import *
from schemas.task import *

tailwind = Script(src="https://cdn.tailwindcss.com")
app, rt = fast_app(hdrs=(tailwind,), debug=True, live=True, reload_interval=1)


@rt('/')
def get():
    task_list: TaskListSchema = TaskList.select().join(TaskListTask).join(Task).where(TaskList.id == 1).first()
    return (
        task_list_view(task_list)
    )


@rt('/add_task')
def post(new_task: str):
    task = Task.create(title=new_task)
    return (
        task_item(task),
        new_task_input_field()
    )


@rt('/task_checkbox')
def put(task_id: int):
    query = Task.update(checked=(Task.checked == 0)).where(Task.id == task_id)
    query.execute()
    task = Task.get(id=task_id)
    return task_checkbox(task)


serve()
