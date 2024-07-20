from __future__ import annotations

import functools
from flask import request as req
from flask import make_response
from flask import jsonify
from typing import Callable, TYPE_CHECKING

from app.config.config import get_config

if TYPE_CHECKING:
    from flask import Response

parser = get_config('config')
project_parser = get_config('project')


def authorization(func: Callable[..., Response]):
    @functools.wraps(func)
    def wrapper():
        query = req.args
        if (
            "project_tk" not in query or 
            "token" not in query
        ):
            return make_response(
                jsonify({
                    "CODE": 403,
                    "MESSAGE": "Forbidden Access. (This IP-Address will be recorded.)"
                })
            )
        
        project_id = query.get("project_id")
        if (
            query.get('project_tk') != project_parser.get(project_id, "token") or
            query.get('token') != parser.get("Default", "token")
        ):
            return make_response(
                jsonify({
                    "CODE": 403,
                    "MESSAGE": "Forbidden Access. (This IP-Address will be recorded.)"
                })
            )

        return func()
    return wrapper