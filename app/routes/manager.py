import datetime

from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request as req

from app.config.config import get_config
from app.validate import authorization, exist_project

try:
    import dbus
except ModuleNotFoundError:
    dbus = False  # Systemctl manage disabled.
else:
    from app.models.systemd_package import SystemdPackage

    sysbus = dbus.SystemBus()
    systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
    manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')

    dbus = True  # Systemctl manage enabled.

bp = Blueprint(
    name="manager",
    import_name="manager",
    url_prefix="/"
)
parser = get_config('project')


@bp.route('/status', methods=['GET'])
@exist_project
def get_status():
    query = req.args
    project_id = query.get("project_id")
    project_type = parser.get(project_id, "type")

    if project_type == "systemctl":
        project_package_id = parser.get(project_id, "package_id")
        service = SystemdPackage(sysbus, manager, project_package_id)

        started_time = datetime.datetime.fromtimestamp(service.uptime.real // 1000000)
        now_time = datetime.datetime.now()

        return make_response(
            jsonify({
                "current_memory": service.memory_usage.real,
                "pid": service.pid.real,
                "state": str(service.state),
                "started": started_time.isoformat(),
                "uptime": (now_time - started_time).total_seconds()
            }), 200
        )
    else:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Unknown Project Type."
            }), 400
        )


@bp.route('/restart', methods=['GET'])
@exist_project
@authorization
def post_restart():
    query = req.args
    project_id = query.get("project_id")
    project_type = parser.get(project_id, "type")

    if project_type == "systemctl":
        project_package_id = parser.get(project_id, "package_id")
        service = SystemdPackage(sysbus, manager, project_package_id)
        service.restart()

        return make_response(
            jsonify({
                "status": "OK"
            }), 200
        )
    else:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Unknown Project Type."
            }), 400
        )
