from fastapi import Depends, Form, Query
from pydantic import EmailStr
from server.models.schemas.base.fields import email_field, password_field, username_field
from server.models.schemas.inc.auth import LoginRequestSchema, PasswordChangeRequestSchema, SignupRequestSchema
from server.utils.exceptions import raise_422_unprocessable_entity


def username_form_field(username: str = Form(**username_field())) -> str:
    return username


def email_form_field(email: EmailStr = Form(**email_field())) -> EmailStr:
    return email


def password_form_field(password: str = Form(**password_field())) -> str:
    return password


def temporary_url_key(
    validation_key: str = Query(
        ...,
        alias="key",
        validation_alias="key",
        title="Validation key",
        description="Validation key included as query parameter in the link sent to user email.",
    ),
):
    return validation_key


def new_password_form_field(
    new_password: str = Form(
        **password_field(
            alias="newPassword",
            validation_alias="newPassword",
            title="New password",
            description="New password to replace the old one.",
        ),
    ),
) -> str:
    return new_password


def repeat_password_form_field(
    repeat_password: str = Form(
        **password_field(
            alias="repeatPassword",
            validation_alias="repeatPassword",
            title="Repeat password",
            description="Repeat password to confirm password.",
        ),
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


def password_change_form(
    password: str = Depends(password_form_field),
    new_password: str = Depends(new_password_form_field),
    repeat_password: str = Depends(repeat_password_form_field),
) -> PasswordChangeRequestSchema:
    if new_password != repeat_password:
        raise_422_unprocessable_entity("Passwords do not match.")
    return PasswordChangeRequestSchema(current_password=password, new_password=new_password)


def password_reset_request_form(
    new_password: str = Depends(new_password_form_field),
    repeat_password: str = Depends(repeat_password_form_field),
) -> str:
    if new_password != repeat_password:
        raise_422_unprocessable_entity("Passwords do not match.")
    return new_password
