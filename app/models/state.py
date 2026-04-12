from enum import Enum


class ProjectState(Enum):
    RUNNING = 0
    RELOADING = 12
    STOPPED = 13
    FAILED = 14
    LOADING = 15
    UNLOADING = 16
    UNKNOWN = 17

    @classmethod
    def from_systemd_state(cls, value: str) -> "ProjectState":
        mapping = {
            "active":       cls.RUNNING,
            "reloading":    cls.RELOADING,
            "inactive":     cls.STOPPED,
            "failed":       cls.FAILED,
            "activating":   cls.LOADING,
            "deactivating": cls.UNLOADING,
        }
        return mapping.get(value, cls.UNKNOWN)


    @classmethod
    def from_docker_state(cls, value: str) -> "ProjectState":
        mapping = {
            "running":    cls.RUNNING,
            "restarting": cls.RELOADING,
            "created":    cls.STOPPED,
            "exited":     cls.STOPPED,
            "paused":     cls.STOPPED,
            "dead":       cls.FAILED,
            "removing":   cls.UNLOADING,
        }
        return mapping.get(value, cls.UNKNOWN)
