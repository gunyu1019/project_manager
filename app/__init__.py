import importlib.util
import logging
import os

from flask import Flask
from app.directory import directory


def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    log = logging.getLogger("app.create_app")

    routes = [
        "app.routes." + file[:-3] for file in os.listdir(
            os.path.join(directory, "routes")
        ) if file.endswith(".py")
    ]
    for route in routes:
        spec = importlib.util.find_spec(route)
        if spec is None:
            log.error("Extension Not Found: {0}".format(route))
            continue

        lib = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(lib)  # type: ignore
        except Exception as e:
            log.exception(e)
            continue

        try:
            blueprint = getattr(lib, 'bp')
        except AttributeError:
            log.error("No Entry Point Error: {0}".format(route))
            continue

        try:
            app.register_blueprint(blueprint)
        except Exception as e:
            log.exception(e)
            continue

    return app