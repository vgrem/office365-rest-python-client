from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.management.managed.app.registration import ManagedAppRegistration
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class DeviceAppManagement(Entity):
    """Singleton entity that acts as a container for all device and app management functionality."""

    @odata(name="managedAppRegistrations")
    @property
    def managed_app_registrations(self):
        """"""
        return self.properties.get(
            "managedAppRegistrations",
            EntityCollection(
                self.context,
                ManagedAppRegistration,
                ResourcePath("managedAppRegistrations", self.resource_path),
            ),
        )
