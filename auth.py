from workos import WorkOSClient

from settings import env

workos_client = WorkOSClient(api_key=env.workos_api_key, client_id=env.workos_client_id)


def get_login_url() -> str:
    provider = "GoogleOAuth"
    redirect_uri = f"{env.domain}/auth/callback"

    authorization_url = workos_client.sso.get_authorization_url(
        provider=provider, redirect_uri=redirect_uri
    )

    return authorization_url
