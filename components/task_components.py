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
            id='new_task',
            placeholder='new task',
            hx_post='/add_task',
            hx_trigger=f'keyup[{ENTER_KEY_CODE}]',
            hx_target='#new_task',
            hx_swap='outerHTML transition:true',
            hx_vals=f'{{"tasklist_id": "{tasklist_id}"}}',
            hx_transition_in='fade-in-scale-up',
            cls='my-3'
        ),)


def task_list_view(task_list: TaskListSchema):
    return (
        Div(
            Div(
                P(task_list.title, cls='text-gray-500 font-bold'),
                Div(cls='absolute top-10 left-0 right-0 h-[2px] bg-black bg-gray-500'),
                cls='relative'
            ),
            Br(),
            Ul(
                *[task_item(task) for task in task_list.tasks],
                new_task_input_field(task_list.id),
                cls='text-2xl',
                id='task_list'
            ),
            cls='pt-10 pl-10 text-2xl w-1/6'
        )
    )
