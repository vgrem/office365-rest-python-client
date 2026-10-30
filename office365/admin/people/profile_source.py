from __future__ import annotations

from typing import Optional

from office365.directory.profile_source_localization import ProfileSourceLocalization
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata


class ProfileSource(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="kind")
    @property
    def kind(self) -> Optional[str]:
        """Gets the kind property"""
        return self.properties.get("kind", None)

    @odata(name="localizations")
    @property
    def localizations(self) -> ClientValueCollection[ProfileSourceLocalization]:
        """Gets the localizations property"""
        return self.properties.get(
            "localizations", ClientValueCollection[ProfileSourceLocalization](ProfileSourceLocalization)
        )

    @odata(name="sourceId")
    @property
    def source_id(self) -> Optional[str]:
        """Gets the sourceId property"""
        return self.properties.get("sourceId", None)

    @odata(name="webUrl")
    @property
    def web_url(self) -> Optional[str]:
        """Gets the webUrl property"""
        return self.properties.get("webUrl", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ProfileSource"
