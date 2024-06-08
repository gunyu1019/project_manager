from __future__ import annotations

import functools
from flask import request as req
from flask import make_response
from flask import jsonify
from typing import Callable, TYPE_CHECKING

from app.config.config import get_config

if TYPE_CHECKING:
    from flask import Response

project_parser = get_config('project')


def exist_project(func: Callable[..., Response]):
    @functools.wraps(func)
    def wrapper():
        query = req.args
        if (
            "project_id" not in query or 
            not project_parser.has_section(query.get('project_id'))
        ):
            return make_response(
                jsonify({
                    "CODE": 400,
                    "MESSAGE": "Missing project ID."
                })
            )

        return func()
    return wrapper