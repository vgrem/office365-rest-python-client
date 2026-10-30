from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.directory.permissions.email_identity import EmailIdentity
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.security.attacksimulations.endusernotificationtype import EndUserNotificationType
from office365.security.attacksimulations.simulationcontentsource import SimulationContentSource
from office365.security.attacksimulations.simulationcontentstatus import SimulationContentStatus

if TYPE_CHECKING:
    from office365.security.end_user_notification_detail import (
        EndUserNotificationDetail,
    )


class EndUserNotification(Entity):
    @odata(name="createdBy")
    @property
    def created_by(self) -> EmailIdentity:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", EmailIdentity())

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="lastModifiedBy")
    @property
    def last_modified_by(self) -> EmailIdentity:
        """Gets the lastModifiedBy property"""
        return self.properties.get("lastModifiedBy", EmailIdentity())

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="notificationType")
    @property
    def notification_type(self) -> EndUserNotificationType:
        """Gets the notificationType property"""
        return self.properties.get("notificationType", EndUserNotificationType.unknown)

    @odata(name="source")
    @property
    def source(self) -> SimulationContentSource:
        """Gets the source property"""
        return self.properties.get("source", SimulationContentSource.unknown)

    @odata(name="status")
    @property
    def status(self) -> SimulationContentStatus:
        """Gets the status property"""
        return self.properties.get("status", SimulationContentStatus.unknown)

    @odata(name="supportedLocales")
    @property
    def supported_locales(self) -> StringCollection:
        """Gets the supportedLocales property"""
        return self.properties.get("supportedLocales", StringCollection())

    @odata(name="details", navigation=True)
    @property
    def details(self) -> EntityCollection[EndUserNotificationDetail]:
        """Gets the details property"""
        from office365.security.end_user_notification_detail import (
            EndUserNotificationDetail,
        )

        return self.properties.get(
            "details",
            EntityCollection[EndUserNotificationDetail](
                self.context, EndUserNotificationDetail, ResourcePath("details", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EndUserNotification"
