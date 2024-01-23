from functools import lru_cache
from typing import Any

from fastapi.templating import Jinja2Templates


@lru_cache()
def config_templates() -> Jinja2Templates:
    return Jinja2Templates(directory="server/templates")


def build_mail_body(context: dict[str, Any], template_name: str) -> str:
    template_server: Jinja2Templates = config_templates()
    template = template_server.TemplateResponse(name=template_name, context=context)
    return template.body.decode("utf-8")
