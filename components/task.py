from fasthtml.common import Input

from constants import ENTER_KEY_CODE

new_task_input = Input(
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
),
