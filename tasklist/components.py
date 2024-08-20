from fasthtml.common import Div, Span, Input, Br, Ul

from constants import ENTER_KEY_CODE
from tasklist.schemas import TaskListSchema
from task.components import task_component, new_task_input_component


def tasklist_title_component(tasklist: TaskListSchema):
    item_id = f'task_title_{tasklist.id}'
    return Div(
        Span(
            "x",
            hx_delete=f'/tasklist/{tasklist.id}',
            hx_trigger=f'click',
            hx_target=f'#tasklist_{tasklist.id}',
            hx_swap='delete transition:true',
            hx_transition_in='fade-in-scale-up',
            cls='flex items-center text-red-300 cursor-pointer '
        ),
        Input(
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
            cls='text-gray-500 font-bold border-none !m-0 !pl-1.5'
        ),
        cls='flex !m-0'
    )


def new_tasklist_title_component(space_id: int):
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


def tasklist_component(tasklist: TaskListSchema):
    return (
        Div(
            tasklist_title_component(tasklist),
            Br(),
            Ul(
                *[task_component(task) for task in tasklist.tasks],
                new_task_input_component(tasklist.id),
                cls='text-2xl',
                id='tasklist'
            ),
            id=f'tasklist_{tasklist.id}',
            cls='text-2xl w-1/5'
        )
    )
