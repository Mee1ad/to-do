from fasthtml.common import *


def input_text_component(**kwargs):
    return (
        Input(
            type='text',
            **kwargs,
            cls='flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background'
                ' file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground'
                ' focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2'
                ' disabled:cursor-not-allowed disabled:opacity-50 flex-grow',
        )
    )


def plus_button_component(**kwargs):
    return (
        Button(
            I(cls='fa-regular fa-plus text-gray-100'),
            type='submit',
            **kwargs,
            cls='inline-flex items-center justify-center whitespace-nowrap'
                ' transition-colors text-primary-foreground bg-primary hover:bg-primary/90 h-9 rounded-md px-3'
        )
    )


def add_form_component(**kwargs):
    return (
        Div(
            input_text_component(),
            plus_button_component(),
            **kwargs,
            cls='flex gap-2',
        )
    )
