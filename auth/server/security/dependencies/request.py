from fastapi import Depends, Form
from pydantic import EmailStr
from server.models.schemas.base.fields import email_field, password_field, username_field
from server.models.schemas.inc.auth import SignupRequestSchema
from server.utils.exceptions import raise_422_unprocessable_entity


def username_form_field(username: str = username_field(Form)) -> str:
    return username


def email_form_field(email: EmailStr = email_field(Form)) -> EmailStr:
    return email


def password_form_field(password: str = password_field(Form)) -> str:
    return password


def repeat_password_form_field(
    repeatPassword: str = Form(
        title="Repeat password",
        description="Repeat password to confirm password.",
        example="Admin@12345",
    ),
) -> str:
    return repeatPassword


def signup_form(
    username: str = Depends(username_form_field),
    email: EmailStr = Depends(email_form_field),
    password: str = Depends(password_form_field),
    repeat_password: str = Depends(repeat_password_form_field),
) -> SignupRequestSchema:
    if password != repeat_password:
        raise_422_unprocessable_entity("Passwords do not match.")
    return SignupRequestSchema(username=username, email=email, password=password)
