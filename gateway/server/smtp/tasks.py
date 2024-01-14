from fastapi import Request

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
