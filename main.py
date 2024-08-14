from fasthtml.common import *

from components.task import new_task_input, task_list

tailwind = Script(src="https://cdn.tailwindcss.com")
app, rt = fast_app(hdrs=(tailwind,), debug=True, live=True, reload_interval=0.5)

tasks = ['task 1', 'task 2', 'task 3']


@rt('/')
def get():
    return (
        task_list(tasks)
    )


@rt('/add_task')
def post(new_task: str):
    tasks.append(new_task)
    return (
        Li(new_task, cls='list-none'),
        new_task_input()
    )


serve()
