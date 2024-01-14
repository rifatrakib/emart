from fastapi import Query


def temporary_url_key(
    key: str = Query(
        ...,
        title="Validation key",
        description="Validation key included as query parameter in the link sent to user email.",
    ),
):
    return key
