from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection


class FederatedIdentityCredential(Entity):
    @property
    def audiences(self) -> StringCollection:
        """Gets the audiences property"""
        return self.properties.get("audiences", StringCollection(None))

    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def issuer(self) -> Optional[str]:
        """Gets the issuer property"""
        return self.properties.get("issuer", None)

    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @property
    def subject(self) -> Optional[str]:
        """Gets the subject property"""
        return self.properties.get("subject", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FederatedIdentityCredential"
