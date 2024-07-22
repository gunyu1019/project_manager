from __future__ import annotations

import functools
from typing import Callable, TYPE_CHECKING

from flask import jsonify
from flask import make_response
from flask import request as req

from app.config.config import get_config

if TYPE_CHECKING:
    from flask import Response

parser = get_config("config")
project_parser = get_config("project")


def authorization(func: Callable[..., Response]):
    @functools.wraps(func)
    def wrapper():
        args = req.args
        headers = req.headers

        if "Project-Token" not in headers or "Token" not in headers:
            return make_response("43", 403)  # Forbidden Access.

        project_id = args.get("project_id")
        if headers.get("Project-Token") != project_parser.get(
            project_id, "token"
        ) or headers.get("Token") != parser.get("Default", "token"):
            return make_response("43", 403)  # Forbidden Access.

        return func()

    return wrapper
