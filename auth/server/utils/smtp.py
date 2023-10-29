from functools import lru_cache
from typing import Any, Dict, List

from fastapi import Request
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr, HttpUrl

from server.config.factory import settings
from server.models.database.users import Account
from server.utils.html import build_mail_body


@lru_cache()
def config_smtp_server() -> ConnectionConfig:
    return ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
        MAIL_STARTTLS=settings.MAIL_STARTTLS,
        MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
        USE_CREDENTIALS=settings.USE_CREDENTIALS,
    )


def prepare_message(
    context: Dict[str, Any],
    recipients: List[EmailStr],
    subject: str,
    template_name: str,
) -> MessageSchema:
    return MessageSchema(
        subject=subject,
        recipients=recipients,
        body=build_mail_body(context, template_name),
        subtype=MessageType.html,
    )


async def send_mail(
    context: Dict[str, Any],
    recipients: List[EmailStr],
    subject: str,
    template_name: str,
) -> None:
    smtp_config: ConnectionConfig = config_smtp_server()
    smtp_agent = FastMail(smtp_config)
    message: MessageSchema = prepare_message(
        context=context,
        recipients=recipients,
        subject=subject,
        template_name=template_name,
    )
    await smtp_agent.send_message(message)


async def send_activation_mail(
    request: Request,
    subject: str,
    template: str,
    url: HttpUrl,
    user: Account,
) -> None:
    context = {
        "request": request,
        "subject": subject,
        "url": url,
        "username": user.username,
    }

    await send_mail(
        context=context,
        recipients=[user.email],
        subject=subject,
        template_name=f"{template}.html",
    )
