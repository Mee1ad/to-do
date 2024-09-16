from fasthtml.common import Div, Span, Input, Fieldset, Legend, Form, I, Button, Script

from constants import ENTER_KEY_CODE
from task.components import TaskCard, TaskInput
from tasklist.schemas import TaskListSchema


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


def TasklistTitle(tasklist: TaskListSchema, **kwargs):
    item_id = f'task-title-{tasklist.id}'
    return Input(
        value=tasklist.title,
        type='text',
        id=item_id,
        name='tasklist_title',
        placeholder='Add New List',
        autocomplete='off',
        hx_put='/tasklist/title',
        hx_trigger='change',
        hx_target=f'#{item_id}',
        hx_swap='outerHTML transition:true',
        hx_vals=f'{{"tasklist_id": "{tasklist.id}"}}',
        hx_transition_in='fade-in-scale-up',
        cls='inline text-primary font-bold focus:outline-none text-2xl w-72'
    ),


def NewTasklistTitle(space_id: int):
    new_tasklist_title_id = f'new_task_title_{space_id}'
    return Div(
        Form(
            Input(
                type='text',
                name='tasklist_title',
                placeholder='Add New List',
                autocomplete='off',
                cls='block rounded-md border-0 p-2 px-3 text-gray-900 shadow-sm ring-1 ring-inset'
                    ' ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset'
                    ' sm:text-sm sm:leading-6 w-full'
            ),
            Button(
                I(
                    data_feather='plus',
                    cls='text-secondary'
                ),
                type='submit',
                cls='bg-primary px-3 rounded-md',
            ),
            hx_post='/tasklist',
            hx_trigger='submit',
            hx_target=f'#space_{space_id}',
            hx_swap='beforeend transition:true',
            hx_vals=f'{{"space_id": "{space_id}"}}',
            hx_transition_in='fade-in-scale-up',
            id=new_tasklist_title_id,
            cls='relative flex gap-2',
            **{
                'hx-on:htmx:before-request': "document.getElementById('new_tasklist_title_component').classList.add('opacity-0'); setTimeout(() => document.getElementById('new_tasklist_title_component').remove(), 10)"
            }
        ),
        cls='w-96'
    ), Script('feather.replace();')


def TasklistCard(tasklist: TaskListSchema):
    return Fieldset(
        Input(
            name='tasklists',
            value=tasklist.id,
            type='hidden'
        ),
        Legend('tasklist', cls='sr-only'),
        Div(
            TasklistTitle(tasklist),
            Div(
                I(
                    data_feather='move',
                    cls='cursor-pointer handle opacity-0 group-hover:opacity-100 transition-all'
                ),
                I(
                    data_feather='archive',
                    hx_patch=f'/tasklist/archive/{tasklist.id}',
                    hx_trigger=f'click',
                    hx_target=f'#tasklist_card_{tasklist.id}',
                    hx_swap='delete transition:true',
                    hx_transition_in='fade-in-scale-up',
                    cls='cursor-pointer'
                ),
                I(
                    data_feather='trash',
                    hx_delete=f'/tasklist/{tasklist.id}',
                    hx_trigger=f'click',
                    hx_target=f'#tasklist_card_{tasklist.id}',
                    hx_swap='delete transition:true',
                    hx_transition_in='fade-in-scale-up',
                    cls='cursor-pointer'
                ),
                cls='flex gap-2'
            ),

            cls='flex items-center justify-between mb-8'
        ),

        Div(
            *[TaskCard(task) for task in tasklist.tasks],
            id=f'tasklist_{tasklist.id}',
            hx_patch=f'/tasklist/{tasklist.id}/sort',
            hx_trigger='end',
            hx_swap='none',
            hx_include="[name='tasks']",
            cls='flex flex-col gap-2 md:sortable sm:max-h-32 md:max-h-64 xl:max-h-96 overflow-auto'
        ),
        TaskInput(tasklist.id),
        id=f'tasklist_card_{tasklist.id}',
        cls='flex flex-col gap-2 shadow-md p-4 rounded-lg group'
    ), Script('feather.replace();')
