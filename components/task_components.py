from fasthtml.common import *

from constants import ENTER_KEY_CODE
from schemas.task import *
from db.models.task import *


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


def task_list_title_view(task_list: TaskListSchema):
    item_id = f'task_title_{task_list.id}'
    return Input(
        type='text',
        id=item_id,
        name='task_list_title',
        value=task_list.title,
        placeholder='Add New List',
        autocomplete='off',
        hx_put='/task_list',
        hx_trigger=f'keyup[{ENTER_KEY_CODE}]',
        hx_target=f'#{item_id}',
        hx_swap='outerHTML transition:true',
        hx_vals=f'{{"task_list_id": "{task_list.id}"}}',
        hx_transition_in='fade-in-scale-up',
        cls='text-gray-500 font-bold border-none'
    ),


def new_task_list_title_view(space_id: int):
    item_id = f'new_task_title_{space_id}'
    return Div(
        Input(
            type='text',
            name='task_list_title',
            placeholder='Add New List',
            autocomplete='off',
            hx_post='/task_list',
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


def task_list_view(task_list: TaskListSchema):
    return (
        Div(
            task_list_title_view(task_list),
            Br(),
            Ul(
                *[task_item(task) for task in task_list.tasks],
                new_task_input_field(task_list.id),
                cls='text-2xl',
                id='task_list'
            ),
            cls='text-2xl w-1/5'
        )
    )


def space_view(space: SpaceSchema):
    return (
        Div(
            Ul(
                *[task_list_view(task_list) for task_list in space.task_lists],
                new_task_list_title_view(space.id),
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
