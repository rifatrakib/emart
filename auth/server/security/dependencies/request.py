from fastapi import Depends, Form
from pydantic import EmailStr
from server.models.schemas.base.fields import email_field, password_field, username_field
from server.models.schemas.inc.auth import LoginRequestSchema, SignupRequestSchema
from server.utils.exceptions import raise_422_unprocessable_entity


def username_form_field(username: str = Form(**username_field())) -> str:
    return username


def email_form_field(email: EmailStr = Form(**email_field())) -> EmailStr:
    return email


def password_form_field(password: str = Form(**password_field())) -> str:
    return password


def repeat_password_form_field(
    repeat_password: str = Form(
        validation_alias="repeatPassword",
        **{
            **password_field(),
            "title": "Repeat password",
            "description": "Repeat password to confirm password.",
            "example": "Admin@12345",
        },
    ),
) -> str:
    return repeat_password


def signup_form(
    username: str = Depends(username_form_field),
    email: EmailStr = Depends(email_form_field),
    password: str = Depends(password_form_field),
    repeat_password: str = Depends(repeat_password_form_field),
) -> SignupRequestSchema:
    if password != repeat_password:
        raise_422_unprocessable_entity("Passwords do not match.")
    return SignupRequestSchema(username=username, email=email, password=password)


def login_form(
    username: str = Depends(username_form_field),
    password: str = Depends(password_form_field),
) -> LoginRequestSchema:
    return LoginRequestSchema(username=username, password=password)
