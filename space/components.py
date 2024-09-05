from fasthtml.common import Aside, H3, Nav, P, Span, Ul, Li, Div, Input, Br, A, Form, Label, Button, I, Script

from auth.helper import get_login_url
from auth.schemas import UserSchema
from constants import ENTER_KEY_CODE
from space.schemas import SpaceSchema
from tasklist.components import TasklistCard, NewTasklistTitle


def SpaceCard(space: SpaceSchema):
    try:
        tasklists_view = [TasklistCard(tasklist) for tasklist in space.tasklists]
    except AttributeError as e:
        tasklists_view = []

    js = """
            htmx.onLoad(function(content) {
                var sortables = content.querySelectorAll(".sortable");
                for (var i = 0; i < sortables.length; i++) {
                    var sortable = sortables[i];
                    var sortableInstance = new Sortable(sortable, {
                        animation: 150,
                        ghostClass: 'blue-background-class',
                        
                        onEnd: function (evt) {
                            console.log(evt);
                          }
                    });
                }
            })
    """
    return (
        Div(
            Div(
                *tasklists_view,
                Div(
                    NewTasklistTitle(space.id) if space else None,
                    id='new_tasklist_title_component',
                ),

                id=f'space_{getattr(space, 'id', None)}',
                hx_patch=f'/space/{space.id}/sort',
                hx_trigger='end',
                hx_swap='none',
                hx_include="[name='tasklists']",
                cls='flex flex-wrap gap-6 sortable'
            ),
            hx_patch='/test3',
            hx_trigger='changed',
            id="space",
            cls='ml-64 py-10 pl-6'
        ),

    ), Script(js)


def spaces_list_component_old(spaces: list[SpaceSchema]):
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


def SpaceInput():
    return (
        Form(
            Label('Title', fr='name',
                  cls='absolute -top-2 left-2 inline-block bg-white px-1 text-xs font-medium text-gray-900'),
            Input(type='text', name='space_title', id='space_title', placeholder='New Space', autocomplete='off',
                  cls='block w-full rounded-md border-0 p-2 px-3 text-gray-900 shadow-sm ring-1 ring-inset'
                      ' ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset'
                      ' sm:text-sm sm:leading-6'),
            Button(
                I(cls='fa-plus fa-regular text-secondary'),
                cls='bg-primary px-3.5 rounded-md',
            ),
            hx_post='/space',
            hx_trigger='submit',
            hx_target=f'#space_list',
            hx_swap='beforeend transition:true',
            hx_transition_in='fade-in-scale-up',
            cls='relative flex gap-2',
            **{'hx-on:htmx:after-request': "this.reset()"}
        )
    )


def SpaceTitle(space: SpaceSchema):
    return Div(
        Input(
            name='spaces',
            value=space.id,
            type='hidden'
        ),
        P(
            Span(space.title, cls='mx-2 text-sm font-medium'),
            hx_get=f'/space/{space.id}',
            # hx_replace_url=f'/space/{space.id}/{space.title}',
            hx_trigger=f'click',
            hx_target='#space',
            hx_swap='outerHTML transition:true',
            hx_transition_in='fade-in-scale-up',
            cls='flex items-center px-3 py-2 text-gray-600 transition-colors duration-300 transform'
                '  dark:text-gray-200 '
                ' dark:hover:text-gray-200 hover:text-gray-700 cursor-pointer'
        ),
        I(
            hx_delete=f'/space/{space.id}',
            hx_trigger=f'click',
            hx_target=f'#space-title-{space.id}',
            hx_swap='delete transition:true',
            hx_transition_in='fade-in-scale-up',
            cls='fa-solid fa-trash p-2 mr-2 hover:bg-secondary rounded-md opacity-0 group-hover:opacity-100 '
                'transition-all cursor-pointer'
        ),
        id=f'space-title-{space.id}',
        cls='flex justify-between items-center group hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg'
    )


def ArchiveTitle():
    return Div(
        P(
            Span('Archive', cls='mx-2 text-sm font-medium'),
            hx_get=f'/archive',
            # hx_replace_url=f'/space/{space.id}/{space.title}',
            hx_trigger=f'click',
            hx_target='#space',
            hx_swap='outerHTML transition:true',
            hx_transition_in='fade-in-scale-up',
            cls='flex items-center px-3 py-2 text-gray-600 transition-colors duration-300 transform'
                '  dark:text-gray-200 '
                ' dark:hover:text-gray-200 hover:text-gray-700 cursor-pointer'
        ),
        id=f'archive_menu',
        cls='flex justify-between items-center group hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg'
    )


def SpacesList(spaces: list[SpaceSchema], user: UserSchema):
    login_button_component = A(
        'Login',
        href=get_login_url(),
        cls='relative flex gap-2 hover:bg-secondary py-1 px-2 rounded-md cursor-pointer',
    ),
    if user.name.lower() != 'guest':
        login_button_component = P(
            'Hi ' + user.name.capitalize()
        )

    return (
        Aside(
            Div(
                Nav(
                    Div(
                        P('Spaces', cls='font-bold'),
                        login_button_component,
                        cls='flex justify-between items-center pt-2 pb-4'
                    ),
                    Div(
                        *[SpaceTitle(space) for space in spaces],
                        id='space_list',
                        hx_patch='/space/sort',
                        hx_trigger='end',
                        hx_swap='none',
                        hx_include="[name='spaces']",
                        cls='space-y-3 sortable'
                    ),
                    ArchiveTitle(),
                    cls='space-y-3'
                ),
                cls='flex flex-col justify-between flex-1 mt-6',
            ),
            SpaceInput(),
            cls='flex flex-col w-64 h-screen px-5 overflow-y-auto bg-white border-r rtl:border-r-0 rtl:border-l'
                ' dark:bg-gray-900 dark:border-gray-700 py-2 fixed',
        )
    )
