import base64

from cryptography.fernet import Fernet
from fastapi_sso.sso.base import OpenID

from server.models.database.accounts import Account, Application


def create_oauth_token(account: Account, application: Application) -> str:
    cipher = Fernet(base64.urlsafe_b64encode(bytes.fromhex(application.secret_key)))
    data = OpenID(
        id=str(account.id),
        email=account.email,
        first_name=account.first_name,
        last_name=account.last_name,
        display_name=account.full_name,
        provider="emart",
    ).model_dump_json()
    return cipher.encrypt(data.encode()).decode()
