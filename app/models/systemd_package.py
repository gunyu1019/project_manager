import dbus


SYSTEMD_UNIT = "org.freedesktop.systemd1.Unit"
SYSTEMD_SERVICE = "org.freedesktop.systemd1.Service"

DBUS_PROPERTIES = "org.freedesktop.DBus.Properties"


class SystemdPackage:
    def __init__(
        self, system_bus: dbus.SystemBus, manager: dbus.Interface, package_name: str
    ):
        self.package_name = package_name

        self._system_bus = system_bus
        self._manager = manager

        try:
            self._obj_path = manager.GetUnit(package_name)
        except dbus.DBusException:  # Depends on disk data.
            self._obj_path = manager.LoadUnit(package_name)

        self._service = system_bus.get_object(
            "org.freedesktop.systemd1", object_path=self._obj_path
        )

    @property
    def _property_interface(self) -> dbus.Interface:
        return dbus.Interface(self._service, dbus_interface=DBUS_PROPERTIES)

    @property
    def _unit_interface(self) -> dbus.Interface:
        return dbus.Interface(self._service, dbus_interface=SYSTEMD_UNIT)

    @property
    def id(self) -> dbus.String:
        return self._property_interface.Get(SYSTEMD_UNIT, "Id")

    @property
    def names(self) -> dbus.Array:
        return self._property_interface.Get(SYSTEMD_UNIT, "Names")

    @property
    def state(self) -> dbus.String:
        """Return state of the service.

        The following states are currently defined:
        "active", "reloading", "inactive", "failed", "activating", and "deactivating
        """
        return self._property_interface.Get(SYSTEMD_UNIT, "ActiveState")

    @property
    def memory_usage(self) -> dbus.UInt64:
        return self._property_interface.Get(SYSTEMD_SERVICE, "MemoryCurrent")

    @property
    def tasks_usage(self) -> dbus.UInt64:
        return self._property_interface.Get(SYSTEMD_SERVICE, "TasksCurrent")

    @property
    def pid(self) -> dbus.UInt32:
        return self._property_interface.Get(SYSTEMD_SERVICE, "MainPID")

    @property
    def uptime(self) -> dbus.UInt64:
        return self._property_interface.Get(SYSTEMD_UNIT, "ActiveEnterTimestamp")

    def restart(self, mode="replace"):
        self._unit_interface.Restart(mode)
        return

    def start(self, mode="replace"):
        self._unit_interface.Start(mode)
        return

    def stop(self, mode="replace"):
        self._unit_interface.Stop(mode)
        return
