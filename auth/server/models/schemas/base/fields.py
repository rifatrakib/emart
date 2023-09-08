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
    )


def email_field() -> Dict[str, Any]:
    return dict(
        title="email",
        decription="Unique email that can be used to identify users.",
    )


def password_field() -> Dict[str, Any]:
    return dict(
        title="password",
        decription="""
            Password containing at least 1 uppercase letter, 1 lowercase letter,
            1 number, 1 character that is neither letter nor number, and
            between 8 to 64 characters.
        """.replace("\n", " ").strip(),
        min_length=8,
        max_length=64,
    )
