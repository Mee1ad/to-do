from fasthtml.common import Div, Span, Input, Br, Ul, Fieldset, Legend, Label, P, Button, Svg, Path, Form, I

from constants import ENTER_KEY_CODE
from tasklist.schemas import TaskListSchema
from task.components import task_component, new_task_input_component


def tasklist_title_component_old(tasklist: TaskListSchema):
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


def tasklist_title_component(tasklist: TaskListSchema, **kwargs):
    item_id = f'task_title_{tasklist.id}'
    return Div(
        P(
            tasklist.title,
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
            cls='inline text-primary font-bold'
        ),
        cls='pb-8'
    )


def new_tasklist_title_component(space_id: int):
    item_id = f'new_task_title_{space_id}'
    return (
        Form(
            Input(
                type='text',
                name='tasklist_title',
                placeholder='Add New List',
                autocomplete='off',
                cls='block rounded-md border-0 p-2 px-3 text-gray-900 shadow-sm ring-1 ring-inset'
                    ' ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset'
                    ' sm:text-sm sm:leading-6'
            ),
            Button(
                I(cls='fa-plus fa-regular text-secondary'),
                type='submit',
                cls='bg-primary px-3.5 rounded-md',
            ),
            hx_post='/tasklist',
            hx_trigger='click',
            hx_target=f'#space_{space_id}',
            hx_swap='beforeend transition:true',
            hx_vals=f'{{"space_id": "{space_id}"}}',
            hx_transition_in='fade-in-scale-up',
            id=item_id,
            cls='relative flex gap-2',
            **{'hx-on:htmx:after-request': "this.reset()"}
        ),)


def tasklist_component_old(tasklist: TaskListSchema):
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


def tasklist_component(tasklist: TaskListSchema):
    return (
        Fieldset(
            Legend('tasklist', cls='sr-only'),
            tasklist_title_component(tasklist),
            Div(
                *[task_component(task) for task in tasklist.tasks],
                id=f'tasklist_{tasklist.id}',
                cls='flex flex-col gap-2'
            ),
            new_task_input_component(tasklist.id),
            cls='flex flex-col w-1/5 gap-2 shadow-md p-4 rounded-lg'
        )
    )
