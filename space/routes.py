import uuid

from fasthtml.common import JSONResponse, Div, Input, Script, Form
from pip._internal.network import session
from pydantic import ValidationError

from app_init import app
from auth.helper import get_user_from_session
from auth.models import User, Login
from auth.schemas import UserSchema
from db.helper import get_space_by_id
from space.components import SpaceCard, SpacesList, SpaceTitle
from space.models import Space, SpaceTaskList
from space.schemas import SpaceCreateSchema
from tasklist.models import TaskList
from tasklist.components import TasklistCard, NewTasklistTitle


@app.get('/space/{space_id}')
def get_space(space_id: int):
    space = get_space_by_id(space_id)
    return SpaceCard(space)


@app.get('/space/{space_id}/{space_title}')
def get_public_space(req, space_id: int, space_title: str):
    user: UserSchema = req.scope['user']
    spaces = Space.select().where(Space.user_id == user.id).execute()
    space = get_space_by_id(space_id)
    return SpacesList(spaces, user), SpaceCard(space)


@app.get('/archive')
def get_archive(session):
    user = get_user_from_session(session)
    tasklists = TaskList.select().where(TaskList.user_id == user.id, TaskList.archived == True).execute()
    tasklists_view = [TasklistCard(tasklist) for tasklist in tasklists]
    return (
        Div(
            Div(
                *tasklists_view,
                id=f'archive',
                hx_patch=f'/space/archive/sort',
                hx_trigger='end',
                hx_swap='none',
                hx_include="[name='tasklists']",
                cls='flex flex-wrap gap-6'
            ),
            id="space",
            cls='ml-64 py-10 pl-6'
        ),

    )


@app.get('/space_title_input/{space_id}')
def get_title_input(session, space_id: int):
    user = get_user_from_session(session)
    space = Space.select().where(Space.user_id == user, Space.id == space_id).first()
    return Form(
        Input(
            value=space.title,
            type='text',
            name='space_title',
            autocomplete='off',
            cls='flex text-md justify-between py-2 pl-3 bg-secondary focus:outline-none rounded-lg w-full',
        ),
        hx_put=f'/space/title/{space.id}',
        hx_trigger='submit',
        hx_target=f'#space-title-text-{space.id}',
        hx_swap='outerHTML transition:true',
        hx_vals=f'{{"space_id": "{space.id}"}}',
        id=f'space-title-text-{space.id}',
    )


@app.put('/space/title/{space_id}')
def update_space_title(session, space_id: int, space_title: str):
    user = get_user_from_session(session)
    space = Space.select().where(Space.user_id == user, Space.id == space_id).first()
    space.title = space_title.capitalize()
    space.save()
    return SpaceTitle(space), Script('feather.replace();')


@app.post('/space')
def create_space(req, space_title: str):
    user: UserSchema = req.scope['user']
    try:
        SpaceCreateSchema(title=space_title)
    except ValidationError as e:
        return JSONResponse({"errors": e.errors()}, status_code=400)
    space = Space.create(title=space_title.capitalize(), user_id=user.id)
    return (
        SpaceTitle(space)
    ), Script('feather.replace();')


@app.delete('/space/{space_id}')
def delete_space(space_id: int):
    SpaceTaskList.delete().where(SpaceTaskList.space == space_id).execute()
    Space.delete().where(Space.id == space_id).execute()


@app.patch('/space/sort')
def sort_tasklists(spaces: list[int]):
    for index, space_id in enumerate(spaces):
        Space.update(order=index).where(Space.id == space_id).execute()


@app.patch('/space/sort/{space_id}')
def sort_tasklists(space_id: int, tasklists: list[int]):
    for index, tasklist_id in enumerate(tasklists):
        SpaceTaskList.update(order=index).where(SpaceTaskList.space == space_id,
                                                SpaceTaskList.tasklist == tasklist_id).execute()
