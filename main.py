import uuid

from pydantic import ValidationError

from auth import *
from components.task_components import *
from db.helper import *
from db.models.auth import User, Login
from helper import clear_session
from schemas.auth import UserSchema
from workos import WorkOSClient
from auth import get_login_url

tailwind = Script(src="https://cdn.tailwindcss.com")
app, rt = fast_app(hdrs=(tailwind,), debug=True, live=True, reload_interval=1)

workos_client = WorkOSClient(
    api_key=env.workos_api_key,
    client_id=env.workos_client_id
)


@rt('/')
def get(session):
    user: UserSchema | None = get_user_from_session(session)
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
            A(
                'Login',
                href=get_login_url(),
                cls='flex flex-row'
            ),
        ),
        Div(
            spaces_list_view(spaces),
            space_view(space),
            id='main',
            cls='flex gap-8',
        ),
        cls='pt-10 pl-10'
    )


@rt('/space/{space_id}')
def get(space_id: int):
    space = get_space_by_id(space_id)
    return space_view(space)


@rt('/space/{space_id}/{space_title}')
def get(space_id: int):
    spaces = Space.select()
    space = get_space_by_id(space_id)
    return Div(
        spaces_list_view(spaces),
        space_view(space),
        id='main',
        cls='flex gap-8 pt-10 pl-10',
    )


@rt('/task')
def post(task_text: str, tasklist_id: int):
    try:
        TaskCreateSchema(task_text=task_text, tasklist_id=tasklist_id)
    except ValidationError as e:
        return JSONResponse({"errors": e.errors()}, status_code=400)
    task = Task.create(title=task_text.capitalize())
    tasklist_task = TaskListTask.create(tasklist_id=tasklist_id, task_id=task.id)
    return (
        task_item(task),
        new_task_input_field(tasklist_id)
    )


@rt('/task/{task_id}')
def delete(task_id: int):
    TaskListTask.delete().where(TaskListTask.task == task_id).execute()
    Task.delete().where(Task.id == task_id).execute()


@rt('/task_checkbox')
def put(task_id: int):
    query = Task.update(checked=(Task.checked == 0)).where(Task.id == task_id)
    query.execute()
    task = Task.get(id=task_id)
    return task_checkbox(task)


@rt('/tasklist')
def post(tasklist_title: str, space_id: int, session):
    user: UserSchema = get_user_from_session(session)
    try:
        TaskListCreateSchema(tasklist_title=tasklist_title, space_id=space_id)
    except ValidationError as e:
        return JSONResponse({"errors": e.errors()}, status_code=400)
    tasklist = TaskList.create(title=tasklist_title.capitalize(), user_id=user.id)
    space_tasklist = SpaceTaskList.create(space_id=space_id, tasklist_id=tasklist.id)
    return (
        tasklist_view(tasklist),
        new_tasklist_title_view(tasklist.id),
    )


@rt('/tasklist/{tasklist_id}')
def delete(tasklist_id: int):
    TaskListTask.delete().where(TaskListTask.tasklist == tasklist_id).execute()
    SpaceTaskList.delete().where(SpaceTaskList.tasklist == tasklist_id).execute()
    TaskList.delete().where(TaskList.id == tasklist_id).execute()


@rt('/tasklist')
def put(tasklist_id: int, tasklist_title: str):
    try:
        TaskListUpdateSchema(id=tasklist_id, title=tasklist_title)
    except ValidationError as e:
        return JSONResponse({"errors": e.errors()}, status_code=400)
    TaskList.update(title=tasklist_title.capitalize()).where(TaskList.id == tasklist_id).execute()
    tasklist = TaskList.get(TaskList.id == tasklist_id)
    return tasklist_title_view(tasklist)


@rt('/space')
def post(space_title: str, session):
    user: UserSchema = get_user_from_session(session)
    try:
        SpaceCreateSchema(title=space_title)
    except ValidationError as e:
        return JSONResponse({"errors": e.errors()}, status_code=400)
    space = Space.create(title=space_title.capitalize(), user_id=user.id)
    return (
        Span(
            "x",
            hx_delete=f'/space/{space.id}',
            hx_trigger=f'click',
            hx_target=f'#space_{space.id}',
            hx_swap='delete transition:true',
            hx_transition_in='fade-in-scale-up',
            cls='text-red-300 cursor-pointer'
        ),
        P(space.title,
          hx_get=f'/space/{space.id}/{space.title}',
          hx_trigger=f'click',
          hx_target=f'#space_view',
          hx_swap='outerHTML transition:true',
          hx_transition_in='fade-in-scale-up',
          cls='flex justify-start p-2'
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


@rt('/space/{space_id}')
def delete(space_id: int):
    SpaceTaskList.delete().where(SpaceTaskList.space == space_id).execute()
    Space.delete().where(Space.id == space_id).execute()


@rt('/login')
def get():
    redirect_uri = "https://63d3-78-180-246-205.ngrok-free.app/login_callback"

    authorization_url = workos_client.user_management.get_authorization_url(
        provider='authkit', redirect_uri=redirect_uri
    )

    return RedirectResponse(authorization_url)


@rt('/login_callback')
def get(code: str):
    profile_and_token = workos_client.sso.get_profile_and_token(code)
    profile = profile_and_token.profile
    print('profile', profile.email)

    return RedirectResponse("/")


@rt('/auth/callback')
def get(code: str, session):
    profile_and_token = workos_client.sso.get_profile_and_token(code)
    profile = profile_and_token.profile
    user, created = User.get_or_create(name=profile.first_name, email=profile.email)
    Login.get_or_create(user=user.id, provider=profile.connection_type,
                        connection_id=profile.connection_id, idp_id=profile.idp_id,
                        defaults={'user': user.id, 'provider': profile.connection_type,
                                  'connection_id': profile.connection_id, 'idp_id': profile.idp_id})
    clear_session(session)
    session['user_id'] = user.id
    return RedirectResponse("/")


serve()
