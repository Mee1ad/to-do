from fasthtml.common import Input, Div, Li, Span, Button, I, Form

from task.schemas import TaskSchema


def TaskCheckbox(task: TaskSchema):
    return Input(
        id=f'task-checkbox-{task.id}',
        type='checkbox',
        name='task-check',
        label='Done',
        checked=task.checked,
        hx_put='/task/checkbox',
        hx_trigger='change',
        # hx_target=f'#task-{task.id}',
        hx_vals=f'{{"task_id": "{task}"}}',
        cls='checkbox w-4 h-4'
    ),


def TaskDelete(task: TaskSchema):
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
            TaskCheckbox(task),
            id=f'task_{task.id}',
            cls='flex text-lg justify-between bg-secondary px-2 rounded-md',
        )
    )


def TaskCard(task: TaskSchema):
    return Div(
        Div(
            Input(
                name='tasks',
                value=task.id,
                type='hidden'
            ),
            TaskCheckbox(task),
            Input(
                value=task.title,
                type='text',
                name='task_title',
                autocomplete='off',
                hx_put='/task/title',
                hx_trigger='change',
                hx_target=f'#task-title-{task.id}',
                # hx_swap='outerHTML transition:true',
                hx_vals=f'{{"task_id": "{task.id}"}}',
                id=f'task-title-{task.id}',
                cls='text-lg px-2 bg-secondary focus:outline-none group',
            ),
            cls='flex items-center'
        ),
        Div(
            I(
                data_feather='move',
                cls='hover:bg-secondary rounded-md opacity-0 group-hover:opacity-30 transition-all duration-300'
                    ' transition-all cursor-pointer handle'
            ),
            I(
                data_feather='trash',
                hx_delete=f'/task/{task.id}',
                hx_trigger=f'click',
                hx_target=f'#task-{task.id}',
                hx_swap='delete transition:true',
                hx_transition_in='fade-in-scale-up',
                cls='hover:bg-secondary rounded-md opacity-0 group-hover:opacity-100 transition-all duration-300'
                    ' transition-all cursor-pointer'
            ),
            cls='flex gap-1'
        ),

        id=f'task-{task.id}',
        cls='flex items-center justify-between bg-secondary px-2 py-1 rounded-md cursor-grab group'
            ' transition-all duration-300'
    )


def TaskInput(tasklist_id: int):
    return (
        Form(
            Input(type='text',
                  name='task_text',
                  id='task_text',
                  placeholder='New Task',
                  autocomplete='off',
                  cls='block w-full rounded-md border-0 p-2 px-3 text-gray-900 shadow-sm ring-1 ring-inset'
                      ' ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset'
                      ' sm:text-sm sm:leading-6'),
            Button(
                I(
                    data_feather='plus',
                    cls='text-secondary'),
                type='submit',
                cls='bg-primary px-3 rounded-md',
            ),
            hx_post='/task',
            hx_trigger='submit',
            hx_target=f'#tasklist_{tasklist_id}',
            hx_swap='beforeend transition:true',
            hx_vals=f'{{"tasklist_id": "{tasklist_id}"}}',
            hx_transition_in='fade-in-scale-up',
            cls='relative flex gap-2',
            **{'hx-on:htmx:after-request': "this.reset()"}
        )
    )
