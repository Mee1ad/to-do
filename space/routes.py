from fasthtml.common import JSONResponse, P, Input
from pydantic import ValidationError

from app_init import app
from auth.helper import get_user_from_session
from auth.schemas import UserSchema
from constants import ENTER_KEY_CODE
from db.helper import get_space_by_id
from space.components import space_component
from space.models import Space, SpaceTaskList
from space.schemas import SpaceCreateSchema


@app.get('/space/{space_id}')
def get_space(space_id: int):
    space = get_space_by_id(space_id)
    return space_component(space)


@app.get('/space/{space_id}/{space_title}')
def get_public_space(space_id: int, space_title: str):
    space = get_space_by_id(space_id)
    return space_component(space)


@app.post('/space')
def create_space(space_title: str, session):
    user: UserSchema = get_user_from_session(session)
    try:
        SpaceCreateSchema(title=space_title)
    except ValidationError as e:
        return JSONResponse({"errors": e.errors()}, status_code=400)
    space = Space.create(title=space_title.capitalize(), user_id=user.id)
    return (
        P(space.title,
          hx_get=f'/space/{space.id}/{space.title}',
          hx_trigger=f'click',
          hx_target=f'#space_component',
          hx_swap='outerHTML transition:true',
          hx_transition_in='fade-in-scale-up',
          cls='p-2'
          ),
        Input(
            type='text',
            name='space_title',
            id='new_space',
            placeholder='Add Space',
            autocomplete='off',
            hx_post='/space',
            hx_trigger=f'keyup[{ENTER_KEY_CODE}]',
            hx_target=f'#space_list',
            hx_swap='beforeend transition:true',
            hx_transition_in='fade-in-scale-up',
            cls='border-none focus:border-none !p-2'
        )

    )


@app.delete('/space/{space_id}')
def delete_space(space_id: int):
    SpaceTaskList.delete().where(SpaceTaskList.space == space_id).execute()
    Space.delete().where(Space.id == space_id).execute()
