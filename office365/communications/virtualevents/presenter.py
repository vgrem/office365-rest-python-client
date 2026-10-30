from __future__ import annotations

from typing import Optional

from office365.communications.virtualevents.presenter_details import VirtualEventPresenterDetails
from office365.directory.permissions.identity import Identity
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class VirtualEventPresenter(Entity):
    """Represents information about a presenter of a virtual event."""

    @odata(name="email")
    @property
    def email(self) -> Optional[str]:
        """Gets the email property"""
        return self.properties.get("email", None)

    @odata(name="identity")
    @property
    def identity(self) -> Identity:
        """Gets the identity property"""
        return self.properties.get("identity", Identity())

    @odata(name="presenterDetails")
    @property
    def presenter_details(self) -> VirtualEventPresenterDetails:
        """Gets the presenterDetails property"""
        return self.properties.get("presenterDetails", VirtualEventPresenterDetails())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VirtualEventPresenter"
