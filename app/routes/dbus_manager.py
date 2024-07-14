
from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request as req

from app.config.config import get_config
from app.directory import directory
from app.validate import exist_project

try:
    import dbus
except ModuleNotFoundError:
    raise ModuleNotFoundError("The dbus package was not found. Disable systemd control.")

bp = Blueprint(
    name="dbus_manager",
    import_name="dbus_manager",
    url_prefix="/"
)
parser = get_config('project')

sysbus = dbus.SystemBus()
systemd1 = sysbus.get_object('org.freedesktop.systemd1',  '/org/freedesktop/systemd1')
manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')


async def systemctl_status(package_name: str):
    return


async def systemctl_restart():
    pass


@bp.route('/status', methods=['GET'])
@exist_project
async def get_status():
    query = req.args
    
