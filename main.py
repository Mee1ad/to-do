from fasthtml.common import *

from components.task import new_task_input

tailwind = Script(src="https://cdn.tailwindcss.com")
app, rt = fast_app(hdrs=(tailwind,), debug=True, live=True, reload_interval=0.5)

tasks = ['task 1', 'task 2', 'task 3']


@rt('/')
def get():
    return (
        Ul(
            *[Li(task, cls='list-none') for task in tasks],
            new_task_input,
            cls='p-10 text-2xl ',
            id='task_list',
        )
    )


@rt('/add_task')
def post(new_task: str):
    tasks.append(new_task)
    return (
        Li(new_task, cls='list-none'),
        new_task_input
    )


serve()
