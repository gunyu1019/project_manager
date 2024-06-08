import git

from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request as req

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
async def post_deploy():
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
    origin = repository.remotes.origin
    result = origin.pull()

    # 64 = Update (Success)
    # 4 = Already to Update


    return make_response(
        jsonify({
            "CODE": 200,
            "MESSAGE": "Success Deployment"
        }), 200
    )
