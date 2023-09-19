from typing import Callable, Union

from fastapi import Depends, Form, Query
from pydantic import EmailStr
from server.models.schemas.base.fields import birth_date_field, email_field, gender_field, name_field, password_field, username_field
from server.models.schemas.inc.auth import LoginRequestSchema, PasswordChangeRequestSchema, SignupRequestSchema
from server.models.schemas.inc.profile import ProfileCreateSchema, ProfileUpdateSchema
from server.utils.enums import Gender
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
        title="Validation key",
        description="Validation key included as query parameter in the link sent to user email.",
    ),
):
    return validation_key


def new_password_form_field(
    newPassword: str = Form(
        **password_field(
            title="New password",
            description="New password to replace the old one.",
        ),
    ),
) -> str:
    return newPassword


def repeat_password_form_field(
    repeatPassword: str = Form(
        **password_field(
            title="Repeat password",
            description="Repeat password to confirm password.",
        ),
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


def first_name_form_field(optional: bool = False) -> Callable:
    def _first_name_form_field(
        firstName: str = Form(
            None if optional else ...,
            **name_field(place="first", max_length=64),
        ),
    ) -> str:
        return firstName

    return _first_name_form_field


def middle_name_form_field(
    middleName: str = Form(
        default=None,
        **name_field(place="middle", max_length=256),
    ),
) -> str:
    return middleName


def last_name_form_field(optional: bool = False) -> Callable:
    def _last_name_form_field(
        lastName: str = Form(
            None if optional else ...,
            **name_field(place="last", max_length=64),
        ),
    ) -> str:
        return lastName

    return _last_name_form_field


def birth_date_form_field(optional: bool = False) -> Callable:
    def _birth_date_form_field(
        birthDate: str = Form(
            None if optional else ...,
            **birth_date_field(),
        ),
    ) -> str:
        return birthDate

    return _birth_date_form_field


def address_form_field(optional: bool = False) -> Callable:
    def _address_form_field(
        address: str = Form(
            None if optional else ...,
            **birth_date_field(),
        ),
    ) -> str:
        return address

    return _address_form_field


def gender_form_field(optional: bool = False) -> Callable:
    def _gender_form_field(
        gender: Gender = Form(
            None if optional else ...,
            **gender_field(),
        ),
    ) -> Gender:
        return gender

    return _gender_form_field


def profile_create_form(
    first_name: str = Depends(first_name_form_field()),
    middle_name: Union[str, None] = Depends(middle_name_form_field),
    last_name: str = Depends(last_name_form_field()),
    birth_date: Union[str, None] = Depends(birth_date_form_field(optional=True)),
    address: Union[str, None] = Depends(address_form_field(optional=True)),
    gender: Union[Gender, None] = Depends(gender_form_field(optional=True)),
) -> ProfileCreateSchema:
    return ProfileCreateSchema(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        birth_date=birth_date,
        address=address,
        gender=gender,
    )


def profile_update_form(
    first_name: Union[str, None] = Depends(first_name_form_field(optional=True)),
    middle_name: Union[str, None] = Depends(middle_name_form_field),
    last_name: Union[str, None] = Depends(last_name_form_field(optional=True)),
    birth_date: Union[str, None] = Depends(birth_date_form_field(optional=True)),
    address: Union[str, None] = Depends(address_form_field(optional=True)),
    gender: Union[Gender, None] = Depends(gender_form_field(optional=True)),
) -> ProfileUpdateSchema:
    if all(not param for param in (first_name, middle_name, last_name, birth_date, address, gender)):
        raise_422_unprocessable_entity("At least one of the parameters must not be None.")

    return ProfileUpdateSchema(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        birth_date=birth_date,
        address=address,
        gender=gender,
    )
