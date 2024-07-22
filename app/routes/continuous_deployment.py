from typing import List

import git
from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request as req

from app.config.config import get_config
from app.validate import authorization, exist_project

bp = Blueprint(
    name="continuous_deployment", import_name="continuous_deployment", url_prefix="/"
)
project_parser = get_config("project")


@bp.route("/deploy", methods=["GET"])
@exist_project
@authorization
def post_deploy():
    query = req.args
    project_id = query.get("project_id")

    if not project_parser.getboolean(project_id, "auto_contiuous_deployment"):
        return make_response(
            "11", 400
        )  # This project has disabled Automatic Continuous Deployment.

    project_path = project_parser.get(project_id, "directory")
    repository = git.Repo(project_path)
    origin: git.Remote = repository.remotes.origin
    results: List[git.FetchInfo] = origin.pull()

    if len(results) == 0:
        return make_response("12", 400)  # No fetch result.
    result: git.FetchInfo = results[0]

    # 64 = Update (Success)
    # 4 = Already to Update
    if result.flags == git.FetchInfo.HEAD_UPTODATE:
        return make_response("13", 400)  # Already Update
    elif result.flags == git.FetchInfo.ERROR:
        return make_response("14", 400)  # An error occurred during pull request.
    elif (
        result.flags == git.FetchInfo.FAST_FORWARD
        or result.flags == git.FetchInfo.FORCED_UPDATE
        or result.flags == git.FetchInfo.NEW_TAG
        or result.flags == git.FetchInfo.NEW_HEAD
        or result.flags == git.FetchInfo.TAG_UPDATE
    ):
        return make_response("0", 200)  # Success Deployment
    return make_response("15", 400)  # Unknown flags.
