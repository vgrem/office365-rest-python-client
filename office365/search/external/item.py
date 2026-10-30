from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.externalconnectors.acl import Acl
from office365.externalconnectors.external_activity import ExternalActivity
from office365.externalconnectors.external_item_content import ExternalItemContent
from office365.externalconnectors.external_item_information_protection_label import (  # noqa: E501
    ExternalItemInformationProtectionLabel,
)
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class ExternalItem(Entity):
    """An item added to a Microsoft Graph connection."""

    @odata(name="activities", navigation=True)
    @property
    def activities(self) -> EntityCollection[ExternalActivity]:
        """Gets the activities property"""
        return self.properties.get(
            "activities",
            EntityCollection[ExternalActivity](
                self.context, ExternalActivity, ResourcePath("activities", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.ExternalItem"

    @odata(name="acl")
    @property
    def acl(self) -> ClientValueCollection[Acl]:
        """Gets the acl property"""
        return self.properties.get("acl", ClientValueCollection[Acl](Acl))

    @odata(name="content")
    @property
    def content(self) -> Optional[ExternalItemContent]:
        """Gets the content property"""
        return self.properties.get("content", None)

    @odata(name="informationProtectionLabel")
    @property
    def information_protection_label(self) -> Optional[ExternalItemInformationProtectionLabel]:
        """Gets the informationProtectionLabel property"""
        return self.properties.get("informationProtectionLabel", None)
