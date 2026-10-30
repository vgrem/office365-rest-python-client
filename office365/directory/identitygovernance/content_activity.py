from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata
from office365.security.datasecurity.process_content_request import ProcessContentRequest


class ContentActivity(Entity):
    @odata(name="contentMetadata")
    @property
    def content_metadata(self) -> ProcessContentRequest:
        """Gets the contentMetadata property"""
        return self.properties.get("contentMetadata", ProcessContentRequest())

    @odata(name="scopeIdentifier")
    @property
    def scope_identifier(self) -> Optional[str]:
        """Gets the scopeIdentifier property"""
        return self.properties.get("scopeIdentifier", None)

    @odata(name="userId")
    @property
    def user_id(self) -> Optional[str]:
        """Gets the userId property"""
        return self.properties.get("userId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ContentActivity"
