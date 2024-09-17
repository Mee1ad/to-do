from fasthtml import serve, FileResponse

# noinspection PyUnresolvedReferences
from auth.routes import *
from settings import env
from space.routes import *
# noinspection PyUnresolvedReferences
from task.routes import *
from tasklist.routes import *

stage = env.stage.lower()


@app.get('/')
def home_page(req):
    user = req.scope.get('user', None)
    spaces = Space.select().where(Space.user == user.id).order_by(Space.order).execute()
    first_space = Space.select().where(Space.user == user.id).order_by(Space.order).first()
    first_space_id = first_space.id if first_space else None
    space = get_space_by_id(first_space_id)
    return Div(
        Div(
            Div(
                SpacesList(spaces, user),
                cls='hidden md:block'
            ),
            SpaceCard(space),
            cls='flex',
        )

    ), Script('feather.replace();')


#  http://localhost:5002/static/svg/log.svg
@app.get("/static/{name:path}.{ext:static}")
def static(name: str, ext: str):
    return FileResponse(f'static\\{name}.{ext}')


serve()
