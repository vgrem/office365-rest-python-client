from office365.backuprestore.root import BackupRestoreRoot
from office365.booking.business.collection import BookingBusinessCollection
from office365.booking.currency import BookingCurrency
from office365.communications.virtualevents.root import VirtualEventsRoot
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class SolutionsRoot(Entity):
    """The entry point for Microsoft Bookings, virtual event, and business scenario APIs."""

    @odata(name="bookingBusinesses")
    @property
    def booking_businesses(self) -> BookingBusinessCollection:
        """Get a collection of bookingBusiness objects that has been created for the tenant."""
        return self.properties.get(
            "bookingBusinesses",
            BookingBusinessCollection(self.context, ResourcePath("bookingBusinesses", self.resource_path)),
        )

    @odata(name="bookingCurrencies")
    @property
    def booking_currencies(self):
        """Get a list of bookingCurrency objects available to a Microsoft Bookings business"""
        return self.properties.get(
            "bookingCurrencies",
            EntityCollection(
                self.context,
                BookingCurrency,
                ResourcePath("bookingCurrencies", self.resource_path),
            ),
        )

    @odata(name="backupRestore")
    @property
    def backup_restore(self) -> BackupRestoreRoot:
        """Get a Microsoft 365 Backup Storage service in a tenant"""
        return self.properties.get(
            "backupRestore",
            BackupRestoreRoot(self.context, ResourcePath("backupRestore", self.resource_path)),
        )

    @odata(name="virtualEvents")
    @property
    def virtual_events(self) -> VirtualEventsRoot:
        """A collection of virtual events."""
        return self.properties.get(
            "virtualEvents",
            VirtualEventsRoot(
                self.context,
                ResourcePath("virtualEvents", self.resource_path),
            ),
        )
