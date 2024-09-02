import uuid

from fasthtml import serve
from fasthtml.common import A, Div

from auth.helper import get_login_url
from auth.routes import *
from space.components import SpacesList
from space.routes import *
# noinspection PyUnresolvedReferences
from task.routes import *
from tasklist.routes import *


@app.get('/')
def home_page(session):
    user: UserSchema = get_user_from_session(session)
    if not user:
        user: UserSchema = User.create(name='Guest')
        Login.create(user_id=user.id, provider='session', connection_id=uuid.uuid4().hex)
        session['user_id'] = user.id
    spaces = Space.select().where(Space.user_id == user.id).execute()
    first_space = Space.select().where(Space.user_id == user.id).first()
    first_space_id = first_space.id if first_space else None
    space = get_space_by_id(first_space_id)
    return Div(
        Div(
            SpacesList(spaces, user),
            Space(space),
            cls='flex',
        )

    )


serve()
