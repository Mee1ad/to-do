from pydantic import ValidationError

from components.task_components import *
from schemas.task import *
from db.helper import *

tailwind = Script(src="https://cdn.tailwindcss.com")
app, rt = fast_app(hdrs=(tailwind,), debug=True, live=True, reload_interval=1)


@rt('/')
def get():
    spaces = Space.select()
    space = get_space_by_id(1)
    return Div(
        spaces_list_view(spaces),
        space_view(space),
        cls='flex gap-8 pt-10 pl-10',
    )


@rt('/space/{space_id}/{space_title}')
def get(space_id: int, space_title: str):
    space = get_space_by_id(space_id)
    return space_view(space)


@rt('/task')
def post(task_text: str, tasklist_id: int):
    try:
        TaskCreateSchema(task_text=task_text, tasklist_id=tasklist_id)
    except ValidationError as e:
        return JSONResponse({"errors": e.errors()}, status_code=400)
    task = Task.create(title=task_text)
    tasklist_task = TaskListTask.create(tasklist_id=tasklist_id, task_id=task.id)
    return (
        task_item(task),
        new_task_input_field(tasklist_id)
    )


@rt('/task_checkbox')
def put(task_id: int):
    query = Task.update(checked=(Task.checked == 0)).where(Task.id == task_id)
    query.execute()
    task = Task.get(id=task_id)
    return task_checkbox(task)


@rt('/task_list')
def post(task_list_title: str, space_id: int):
    try:
        TaskListCreateSchema(task_list_title=task_list_title, space_id=space_id)
    except ValidationError as e:
        return JSONResponse({"errors": e.errors()}, status_code=400)
    task_list = TaskList.create(title=task_list_title.capitalize())
    space_task_list = SpaceTaskList.create(space_id=space_id, task_list_id=task_list.id)
    return (
        task_list_view(task_list),
        new_task_list_title_view(task_list.id),
    )


@rt('/task_list')
def put(task_list_id: int, task_list_title: str):
    try:
        TaskListUpdateSchema(id=task_list_id, title=task_list_title)
    except ValidationError as e:
        return JSONResponse({"errors": e.errors()}, status_code=400)
    TaskList.update(title=task_list_title.capitalize()).where(TaskList.id == task_list_id).execute()
    task_list = TaskList.get(TaskList.id == task_list_id)
    return task_list_title_view(task_list)


@rt('/space')
def post(space_title: str):
    try:
        SpaceCreateSchema(title=space_title)
    except ValidationError as e:
        return JSONResponse({"errors": e.errors()}, status_code=400)
    space = Space.create(title=space_title.capitalize())
    return (
        P(space.title,
          hx_get=f'/space/{space.id}/{space.title}',
          hx_trigger=f'click',
          hx_target=f'#space_view',
          hx_swap='outerHTML transition:true',
          hx_transition_in='fade-in-scale-up',
          cls='p-2'
          ),
        Input(
            type='text',
            name='task_space',
            id='new_space',
            placeholder='Add Space',
            autocomplete='off',
            hx_post='/space',
            hx_trigger=f'keyup[{ENTER_KEY_CODE}]',
            hx_target=f'#space_list',
            hx_swap='beforeend transition:true',
            hx_transition_in='fade-in-scale-up',
            cls='border-none focus:border-none !p-2'
        )

    )


serve()
