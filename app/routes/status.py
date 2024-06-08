
from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request as req

from app.config.config import get_config
from app.directory import directory

bp = Blueprint(
    name="project_status",
    import_name="project_status",
    url_prefix="/"
)
parser = get_config('project')


async def systemctl_status():
    pass


async def package_manager_status():
    pass


@bp.route('/status', methods=['GET'])
async def get_status():
    query = req.args
    if "project_id" not in query or not parser.has_section(query.get('project_id')):
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Missing project ID."
            })
        )
    
