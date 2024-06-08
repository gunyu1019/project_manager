
from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request as req

from app.config.config import get_config
from app.directory import directory
from app.validate import exist_project

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
@exist_project
async def get_status():
    query = req.args
    
