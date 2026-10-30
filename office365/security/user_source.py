from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata
from office365.security.healthissues.sourcetype import SourceType


class UserSource(Entity):
    @odata(name="email")
    @property
    def email(self) -> Optional[str]:
        """Gets the email property"""
        return self.properties.get("email", None)

    @odata(name="includedSources")
    @property
    def included_sources(self) -> SourceType:
        """Gets the includedSources property"""
        return self.properties.get("includedSources", SourceType.mailbox)

    @odata(name="siteWebUrl")
    @property
    def site_web_url(self) -> Optional[str]:
        """Gets the siteWebUrl property"""
        return self.properties.get("siteWebUrl", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.UserSource"
