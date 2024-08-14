from fasthtml.common import Input, Ul, Li

from constants import ENTER_KEY_CODE


def new_task_input():
    return (
        Input(
            type='text',
            name='new_task',
            id='new_task',
            placeholder='new task',
            hx_post='/add_task',
            hx_trigger=f'keyup[{ENTER_KEY_CODE}]',
            hx_target='#new_task',
            hx_swap='outerHTML transition:true',
            hx_transition_in='fade-in-scale-up',
            cls='my-3'
        ),)


def task_list(tasks):
    return (
        Ul(
            *[Li(task, cls='list-none') for task in tasks],
            new_task_input(),
            cls='p-10 text-2xl ',
            id='task_list'
        )
    )
