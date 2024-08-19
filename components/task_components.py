from fasthtml.common import *

from constants import ENTER_KEY_CODE
from schemas.task import *


def task_checkbox(task: TaskSchema):
    return Input(
        id=f'task-{task.id}',
        type='checkbox',
        name='task-check',
        label='Done',
        checked=task.checked,
        hx_put='/task_checkbox',
        hx_trigger='change',
        hx_target=f'#task-{task.id}',
        hx_vals=f'{{"task_id": "{task}"}}',
        hx_swap='outerHTML',
        cls='mr-0'
    )


def task_item(task: TaskSchema):
    return (
        Div(Li(task.title, cls='list-none'),
            task_checkbox(task),
            cls='flex text-2xl justify-between',
            )
    )


def new_task_input_field(tasklist_id: int):
    return (
        Input(
            type='text',
            name='task_text',
            id=f'new_task_{tasklist_id}',
            placeholder='new task',
            autocomplete='off',
            hx_post='/task',
            hx_trigger=f'keyup[{ENTER_KEY_CODE}]',
            hx_target=f'#new_task_{tasklist_id}',
            hx_swap='outerHTML transition:true',
            hx_vals=f'{{"tasklist_id": "{tasklist_id}"}}',
            hx_transition_in='fade-in-scale-up',
            cls='my-3'
        ),)


def tasklist_title_view(tasklist: TaskListSchema):
    item_id = f'task_title_{tasklist.id}'
    return Input(
        type='text',
        id=item_id,
        name='tasklist_title',
        value=tasklist.title,
        placeholder='Add New List',
        autocomplete='off',
        hx_put='/tasklist',
        hx_trigger=f'keyup[{ENTER_KEY_CODE}]',
        hx_target=f'#{item_id}',
        hx_swap='outerHTML transition:true',
        hx_vals=f'{{"tasklist_id": "{tasklist.id}"}}',
        hx_transition_in='fade-in-scale-up',
        cls='text-gray-500 font-bold border-none'
    ),


def new_tasklist_title_view(space_id: int):
    item_id = f'new_task_title_{space_id}'
    return Div(
        Input(
            type='text',
            name='tasklist_title',
            placeholder='Add New List',
            autocomplete='off',
            hx_post='/tasklist',
            hx_trigger=f'keyup[{ENTER_KEY_CODE}]',
            hx_target=f'#{item_id}',
            hx_swap='outerHTML transition:true',
            hx_vals=f'{{"space_id": "{space_id}"}}',
            hx_transition_in='fade-in-scale-up',
            cls='text-gray-500 text-2xl font-bold border-none'
        ),
        id=item_id,
        cls='w-1/5 min-w-48'
    ),


def tasklist_view(tasklist: TaskListSchema):
    return (
        Div(
            tasklist_title_view(tasklist),
            Br(),
            Ul(
                *[task_item(task) for task in tasklist.tasks],
                new_task_input_field(tasklist.id),
                cls='text-2xl',
                id='tasklist'
            ),
            cls='text-2xl w-1/5'
        )
    )


def space_view(space: SpaceSchema):
    try:
        tasklists_view = [tasklist_view(tasklist) for tasklist in space.tasklists]
    except AttributeError as e:
        tasklists_view = []
    return (
        Div(
            Ul(
                *tasklists_view,
                new_tasklist_title_view(space.id) if space else None,
                cls='flex flex-wrap gap-8'
            ),
            id="space_view",
            cls=''
        )
    )


def spaces_list_view(spaces: list[SpaceSchema]):
    return Aside(
        Nav(
            H3('Spaces', cls='font-bold text-lg'),
            Br(),
            Ul(
                *[
                    Li(
                        P(space.title,
                          hx_get=f'/space/{space.id}/{space.title}',
                          hx_trigger=f'click',
                          hx_target=f'#space_view',
                          hx_swap='outerHTML transition:true',
                          hx_transition_in='fade-in-scale-up',
                          )) for space in spaces],
                Input(
                    type='text',
                    name='space_title',
                    id='new_space',
                    placeholder='Add Space',
                    autocomplete='off',
                    hx_post='/space',
                    hx_trigger=f'keyup[{ENTER_KEY_CODE}]',
                    hx_target=f'#new_space',
                    hx_swap='outerHTML transition:true',
                    hx_transition_in='fade-in-scale-up',
                    cls='border-none focus:border-none !p-2'
                ),
                id='space_list',
                cls='cursor-pointer'
            ),

        ),

        cls='p-10 shadow-lg'
    ),
