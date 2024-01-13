from fastapi import Request

from server.models.database.accounts import Account
from server.smtp.config import send_mail


async def send_activation_mail(request: Request, key: str, account: Account) -> None:
    await send_mail(
        context={
            "request": request,
            "subject": f"Account activation for {account.full_name}",
            "url": f"{request.base_url}api/v1/accounts/activate?key={key}",
            "username": account.username,
        },
        recipients=[account.email],
        template_name="activation.html",
    )
