from abc import ABC, abstractmethod


class BasePackage(ABC):
    def __init__(
        self, package_name: str
    ):
        self.package_name = package_name

    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @property
    @abstractmethod
    def state(self) -> str:
        """Return state of the service.

        The following states are currently defined:
        "active", "reloading", "inactive", "failed", "activating", and "deactivating
        """
        pass

    @property
    @abstractmethod
    def memory_usage(self) -> int:
        pass

    @property
    @abstractmethod
    def tasks_usage(self) -> int:
        pass

    @property
    @abstractmethod
    def pid(self) -> int:
        pass

    @property
    @abstractmethod
    def uptime(self) -> int:
        pass

    @abstractmethod
    def restart(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
