import datetime
import docker
import docker.errors
import docker.models.containers

from typing import Any, Optional
from .base_package import BasePackage


class DockerPackage(BasePackage):
    def __init__(self, container: docker.models.containers.Container, engine: Optional[docker.DockerClient] = False):
        super().__init__(container.name)
        self._container = container
        self._engine = engine

    @classmethod
    def from_container_name(cls, container_name: str, engine: docker.DockerClient) -> "DockerPackage":
        try:
            container = engine.containers.get(container_name)
            return cls(container, engine)
        except docker.errors.NotFound:
            raise KeyError(f"Container {container_name} not found")

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

    def restart(self, rebuild: bool = False):
        if rebuild:
            if not self._engine:
                raise ValueError("Engine is not set")

            _origin_name = self._container.name
            self._container.stop()
            self._container.remove(force=True)

            self._container = self._engine.containers.run(
                f"{_origin_name}:latest",
                name=_origin_name,
                detach=True
            )

        self._container.restart()

    def start(self):
        self._container.start()

    def stop(self):
        self._container.stop()