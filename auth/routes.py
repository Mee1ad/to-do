from fasthtml.common import RedirectResponse

from app_init import app
from auth.helper import workos_client, clear_session
from auth.models import User, Login


@app.get('/auth/callback')
def callback(req, code: str):
    profile_and_token = workos_client.sso.get_profile_and_token(code)
    profile = profile_and_token.profile
    user = User.select().where(User.name == profile.first_name, User.email == profile.email).first()
    if not user:
        redis_session = req.scope['redis_session']
        guest_user_id = redis_session.get('user_id')
        user = User.select().where(User.name == 'Guest', User.id == guest_user_id).first()
        user.name = profile.first_name
        user.email = profile.email
        user.save()
    Login.get_or_create(user=user.id, provider=profile.connection_type,
                        connection_id=profile.connection_id, idp_id=profile.idp_id,
                        defaults={'user': user.id, 'provider': profile.connection_type,
                                  'connection_id': profile.connection_id, 'idp_id': profile.idp_id})

    return RedirectResponse("/")


@app.get('/auth/logout')
def logout(session):
    session.clear()
    return RedirectResponse("/")
