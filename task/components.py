from fasthtml.common import Input, Div, Li, Span, Button, Svg, Path

from constants import ENTER_KEY_CODE
from task.schemas import TaskSchema


def task_checkbox_component(task: TaskSchema):
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


def task_component(task: TaskSchema):
    return (
        Div(
            Li(
                Span(
                    "x",
                    hx_delete=f'/task/{task.id}',
                    hx_trigger=f'click',
                    hx_target=f'#task_{task.id}',
                    hx_swap='delete transition:true',
                    # hx_vals=f'{{"tasklist_id": "{tasklist_id}"}}',
                    hx_transition_in='fade-in-scale-up',
                    cls='text-red-300 cursor-pointer'
                ),
                task.title,
                cls='list-none'
            ),
            task_checkbox_component(task),
            id=f'task_{task.id}',
            cls='flex text-2xl justify-between',
        )
    )


def new_task_input_component(tasklist_id: int):
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



