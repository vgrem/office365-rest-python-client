from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.backuprestore.serviceapps.status import ServiceAppStatus
from office365.entity import Entity
from office365.runtime.converters.scalars import iso_z
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identity_set import IdentitySet
    from office365.directory.permissions.identity import Identity


class ServiceApp(Entity):
    def activate(self, effective_date_time: datetime) -> Self:
        """Activate a third-party backup service app for the tenant.

        Args:
            effective_date_time: The UTC date-time from which the app should be effective.
        """
        payload = {"effectiveDateTime": iso_z(effective_date_time)}
        qry = ServiceOperationQuery(self, "activate", None, payload, None, self)
        self.context.add_query(qry)
        return self

    def deactivate(self) -> Self:
        """Deactivate a third-party backup service app for the tenant."""
        qry = ServiceOperationQuery(self, "deactivate", return_type=self)
        self.context.add_query(qry)
        return self

    @odata(name="application")
    @property
    def application(self) -> Identity:
        """Gets the application property"""
        from office365.directory.permissions.identity import Identity

        return self.properties.get("application", Identity())

    @odata(name="effectiveDateTime")
    @property
    def effective_date_time(self) -> Optional[datetime]:
        """Gets the effectiveDateTime property"""
        return self.properties.get("effectiveDateTime", datetime.min)

    @odata(name="lastModifiedBy")
    @property
    def last_modified_by(self) -> IdentitySet:
        """Gets the lastModifiedBy property"""
        from office365.directory.identity_set import IdentitySet

        return self.properties.get("lastModifiedBy", IdentitySet())

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="registrationDateTime")
    @property
    def registration_date_time(self) -> Optional[datetime]:
        """Gets the registrationDateTime property"""
        return self.properties.get("registrationDateTime", datetime.min)

    @odata(name="status")
    @property
    def status(self) -> ServiceAppStatus:
        """Gets the status property"""
        return self.properties.get("status", ServiceAppStatus.inactive)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ServiceApp"
