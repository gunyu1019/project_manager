import datetime

from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request as req

from app import get_config
from app.models.state import ProjectState
from app.validate import authorization, automatic_exist_project, exist_project

try:
    import dbus
except ModuleNotFoundError:
    dbus = False  # Systemctl manage disabled.

    SystemdPackage = None
    manager = None
else:
    from app.models.packages.systemd_package import SystemdPackage

    sysbus = dbus.SystemBus()
    systemd1 = sysbus.get_object(
        "org.freedesktop.systemd1", "/org/freedesktop/systemd1"
    )
    manager = dbus.Interface(systemd1, "org.freedesktop.systemd1.Manager")

    dbus = True  # Systemctl manage enabled.

try:
    import docker
except ModuleNotFoundError:
    docker = False  # Docker manage disabled.

    DockerPackage = None
    docker_manager = None
else:
    from app.models.packages.docker_package import DockerPackage

    docker_manager = docker.from_env()
    docker = True  # Docker manage enabled.

bp = Blueprint(name="manager", import_name="manager", url_prefix="/")
parser = get_config("project")


@bp.route("/status", methods=["GET"])
@automatic_exist_project
def get_status():
    query = req.args
    project_id = query.get("project_id")
    project_type = parser.get(project_id, "type")

    if project_type == "systemctl" and dbus:
        project_package_id = parser.get(project_id, "package_id")
        service = SystemdPackage(sysbus, manager, project_package_id)

        started_time = datetime.datetime.fromtimestamp(service.uptime.real // 1000000)
        now_time = datetime.datetime.now()

        if str(service.state) == "active":
            return make_response(
                jsonify(
                    {
                        "current_memory": service.memory_usage.real,
                        "pid": service.pid.real,
                        "state": str(service.state),
                        "started": started_time.isoformat(),
                        "uptime": (now_time - started_time).total_seconds(),
                    }
                ),
                200,
            )

        return make_response(jsonify({"state": str(service.state)}), 200)
    else:
        return make_response(
            jsonify({"CODE": 400, "MESSAGE": "Unknown Project Type."}), 400
        )


@bp.route("/state", methods=["GET"])
@automatic_exist_project
def get_state():
    query = req.args
    project_id = query.get("project_id")
    project_type = parser.get(project_id, "type")

    if project_type == "systemctl" and dbus:
        project_package_id = parser.get(project_id, "package_id")
        service = SystemdPackage(sysbus, manager, project_package_id)
        state = ProjectState.from_systemd_state(str(service.state))
        return make_response(f"{state.value}", 200)
    elif project_type == "docker" and docker:
        pass
    else:
        return make_response("11", 400)  # Unknown Project Type.


@bp.route("/restart", methods=["GET", "POST"])
@exist_project
@authorization
def post_restart():
    query = req.args
    project_id = query.get("project_id")
    is_update = query.get(project_id, "is_update", False)
    project_type = parser.get(project_id, "type")

    if project_type == "systemctl" and dbus:
        project_package_id = parser.get(project_id, "package_id")
        service = SystemdPackage(sysbus, manager, project_package_id)
        service.restart()

        return make_response("0", 200)
    else:
        return make_response("11", 400)  # Unknown Project Type.
