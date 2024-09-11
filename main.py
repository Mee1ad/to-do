from fasthtml import serve

# noinspection PyUnresolvedReferences
from auth.routes import *
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
    spaces = Space.select().where(Space.user_id == user.id).order_by(Space.order).execute()
    first_space = Space.select().where(Space.user_id == user.id).order_by(Space.order).first()
    first_space_id = first_space.id if first_space else None
    space = get_space_by_id(first_space_id)
    return Div(
        Div(
            SpacesList(spaces, user),
            SpaceCard(space),
            cls='flex',
        )

    ), Script('feather.replace();')


serve()
