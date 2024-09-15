from fasthtml.common import RedirectResponse

from app_init import app
from auth.helper import workos_client, clear_session
from auth.models import User, Login


@app.get('/auth/callback')
def callback(req, code: str):
    profile_and_token = workos_client.sso.get_profile_and_token(code)
    profile = profile_and_token.profile
    user, created = User.get_or_create(name=profile.first_name, email=profile.email)
    Login.get_or_create(user=user.id, provider=profile.connection_type,
                        connection_id=profile.connection_id, idp_id=profile.idp_id,
                        defaults={'user': user.id, 'provider': profile.connection_type,
                                  'connection_id': profile.connection_id, 'idp_id': profile.idp_id})
    req.scope['redis_session'] = {
        'session_id': req.scope['redis_session']['session_id'],
        'user_id': user.id
    }
    return RedirectResponse("/")


@app.get('/auth/logout')
def logout(session):
    session.clear()
    return RedirectResponse("/")
