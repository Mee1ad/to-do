from fasthtml.common import Aside, H3, Nav, P, Span, Ul, Li, Div, Input, Br

from constants import ENTER_KEY_CODE
from space.schemas import SpaceSchema
from tasklist.components import tasklist_component, new_tasklist_title_component


def space_component(space: SpaceSchema):
    try:
        tasklists_view = [tasklist_component(tasklist) for tasklist in space.tasklists]
    except AttributeError as e:
        tasklists_view = []
    return (
        Div(
            Ul(
                *tasklists_view,
                new_tasklist_title_component(space.id) if space else None,
                cls='flex flex-wrap gap-8'
            ),
            id="space_component",
            cls=''
        )
    )


def spaces_list_component(spaces: list[SpaceSchema]):
    return Aside(
        Nav(
            H3(
                'Spaces',
                hx_get='/',
                hx_replace_url='/',
                hx_trigger='click',
                hx_target='#main',
                hx_swap='outerHTML transition:true',
                cls='font-bold text-lg cursor-pointer'),
            Br(),
            Ul(
                *[
                    Li(
                        Span(
                            "x",
                            hx_delete=f'/space/{space.id}',
                            hx_trigger=f'click',
                            hx_target=f'#space_{space.id}',
                            hx_swap='delete transition:true',
                            hx_transition_in='fade-in-scale-up',
                            cls='text-red-300 cursor-pointer'
                        ),
                        P(space.title, ),
                        id=f'space_{space.id}',
                        hx_get=f'/space/{space.id}',
                        hx_replace_url=f'/space/{space.id}/{space.title}',
                        hx_trigger=f'click',
                        hx_target=f'#space_component',
                        hx_swap='outerHTML transition:true',
                        hx_transition_in='fade-in-scale-up',
                        cls='flex justify-start px-0 gap-4'
                    ) for space in spaces],
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
