from typing import Any, Dict


def username_field() -> Dict[str, Any]:
    return dict(
        title="username",
        decription="""
            Unique username containing letters, numbers, and
            any of (., _, -, @) in between 6 to 32 characters.
        """.replace("\n", " ").strip(),
        pattern=r"^[\w.@_-]{6,32}$",
        min_length=6,
        max_length=32,
        example="superadmin",
    )


def email_field() -> Dict[str, Any]:
    return dict(
        title="email",
        decription="Unique email that can be used to identify users.",
        example="admin@app.io",
    )


def password_field(**kwargs) -> Dict[str, Any]:
    field_attributes = dict(
        title="password",
        decription="""
            Password containing at least 1 uppercase letter, 1 lowercase letter,
            1 number, 1 character that is neither letter nor number, and
            between 8 to 64 characters.
        """.replace("\n", " ").strip(),
        min_length=8,
        max_length=64,
        example="Admin@12345",
    )

    if kwargs:
        field_attributes.update(kwargs)
    return field_attributes


def name_field(**kwargs) -> Dict[str, Any]:
    return dict(
        title=f"{kwargs['place']} name",
        decription=f"{kwargs['place'].title()} name of the user.",
        example="John",
        max_length=kwargs["max_length"],
    )


def address_field() -> Dict[str, Any]:
    return dict(
        title="address",
        decription="Address of the user.",
        example="1234 Main St. New York, NY 10001",
        max_length=1024,
    )


def birth_date_field() -> Dict[str, Any]:
    return dict(
        title="birth date",
        decription="Birth date of the user.",
        example="2000-01-01",
    )


def gender_field() -> Dict[str, Any]:
    return dict(
        title="gender",
        description="Gender of the user.",
        example="m",
    )
