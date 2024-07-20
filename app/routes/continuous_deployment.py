import git
from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request as req
from typing import List

from app.config.config import get_config
from app.validate import authorization, exist_project

bp = Blueprint(
    name="continuous_deployment",
    import_name="continuous_deployment",
    url_prefix="/deploy"
)
project_parser = get_config('project')


@bp.route('/deploy', methods=['GET'])
@exist_project
@authorization
def post_deploy():
    query = req.args
    project_id = query.get("project_id")

    if not project_parser.getboolean(project_id, "auto_contiuous_deployment"):
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "This project has disabled Automatic Continuous Deployment."
            }), 400
        )

    project_path = project_parser.get(project_id, "directory")
    repository = git.Repo(project_path)
    origin: git.Remote = repository.remotes.origin
    origin = origin.update()
    results: List[git.FetchInfo] = origin.pull()

    if len(results) == 0:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "No fetch result."
            }), 400
        )
    result: git.FetchInfo = results[0]

    # 64 = Update (Success)
    # 4 = Already to Update
    if result.flags == git.FetchInfo.HEAD_UPTODATE:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Already updated"
            }), 400
        )
    elif result.flags == git.FetchInfo.ERROR:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "An error occurred during pull request."
            }), 400
        )
    elif (
        result.flags == git.FetchInfo.FAST_FORWARD or
        result.flags == git.FetchInfo.FORCED_UPDATE or
        result.flags == git.FetchInfo.NEW_TAG or
        result.flags == git.FetchInfo.NEW_HEAD or
        result.flags == git.FetchInfo.TAG_UPDATE
    ):
        return make_response(
            jsonify({
                "CODE": 200,
                "MESSAGE": "Success Deployment"
            }), 200
        )
    return make_response(
        jsonify({
            "CODE": 400,
            "MESSAGE": "Unknown flags."
        }), 400
    )
