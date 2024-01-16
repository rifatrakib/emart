from fastapi import Request

from server.models.database.accounts import Account
from server.models.schemas.requests.auth import SignupRequestSchema
from server.smtp.config import send_mail


async def send_activation_mail(request: Request, key: str, account: SignupRequestSchema) -> None:
    await send_mail(
        context={
            "request": request,
            "subject": f"Account activation for {account.first_name} {account.last_name}",
            "url": f"{request.base_url}api/v1/accounts/activate?key={key}",
            "username": account.username,
        },
        recipients=[account.email],
        template_name="activation.html",
    )


async def send_forgot_password_mail(request: Request, key: str, account: Account) -> None:
    await send_mail(
        context={
            "request": request,
            "subject": f"Password reset request for {account.username}",
            "url": f"{request.base_url}api/v1/accounts/password/reset?key={key}",
            "username": account.username,
        },
        recipients=[account.email],
        template_name="forgot-password.html",
    )


async def send_email_update_mail(request: Request, key: str, account: Account) -> None:
    await send_mail(
        context={
            "request": request,
            "subject": f"Email update request for {account.username}",
            "url": f"{request.base_url}api/v1/accounts/email/update?key={key}",
            "username": account.username,
        },
        recipients=[account.email],
        template_name="update-email.html",
    )
