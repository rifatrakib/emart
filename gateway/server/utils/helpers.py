from server.config.factory import settings


def create_tags(tags: list[str]) -> list[str]:
    return [f"{settings.APP_NAME}: {tag}" for tag in tags]
