import datetime
import docker.models.containers

from typing import Any
from .base_package import BasePackage


class DockerPackage(BasePackage):
    def __init__(self, container: docker.models.containers.Container):
        super().__init__(container.name)
        self._container = container

    @property
    def id(self) -> str:
        return self._container.id

    @property
    def state(self) -> str:
        """Return state of the service.

        The following states are currently defined:
        "created", "restarting", "running", "removing", "paused", "exited", and "dead" """
        return self._container.status

    @property
    def _stats(self) -> dict[str, Any]:
        return self._container.stats(stream=False)

    @property
    def memory_usage(self) -> int:
        return self._stats["memory_stats"]["usage"]

    @property
    def tasks_usage(self) -> int:
        return self._stats["pids_stats"]["current"]

    @property
    def pid(self) -> int:
        return self._container.attrs["State"]["Pid"]

    @property
    def uptime(self) -> int:
        return int(datetime.datetime.fromtimestamp(self._container.attrs["State"]["StartedAt"]).timestamp())

    def restart(self):
        self._container.restart()

    def start(self):
        self._container.start()

    def stop(self):
        self._container.stop()