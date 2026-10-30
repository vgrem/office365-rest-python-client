from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.security.attacksimulations.simulationcontentsource import SimulationContentSource
from office365.security.attacksimulations.simulationcontentstatus import SimulationContentStatus

if TYPE_CHECKING:
    from office365.directory.permissions.email_identity import EmailIdentity
    from office365.security.attacksimulations.landing_page_detail import (
        LandingPageDetail,
    )


class LandingPage(Entity):
    """Represents an attack simulation landing page."""

    @odata(name="createdBy")
    @property
    def created_by(self) -> EmailIdentity:
        """Gets the createdBy property"""
        from office365.directory.permissions.email_identity import EmailIdentity

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
        from office365.directory.permissions.email_identity import EmailIdentity

        return self.properties.get("lastModifiedBy", EmailIdentity())

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="locale")
    @property
    def locale(self) -> Optional[str]:
        """Gets the locale property"""
        return self.properties.get("locale", None)

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
    def details(self) -> EntityCollection[LandingPageDetail]:
        """Gets the details property"""
        from office365.security.attacksimulations.landing_page_detail import (
            LandingPageDetail,
        )

        return self.properties.get(
            "details",
            EntityCollection[LandingPageDetail](
                self.context, LandingPageDetail, ResourcePath("details", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.LandingPage"
