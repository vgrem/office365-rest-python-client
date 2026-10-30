from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class IosVppEBook(Entity):
    @odata(name="appleId")
    @property
    def apple_id(self) -> Optional[str]:
        """Gets the appleId property"""
        return self.properties.get("appleId", None)

    @odata(name="genres")
    @property
    def genres(self) -> StringCollection:
        """Gets the genres property"""
        return self.properties.get("genres", StringCollection())

    @odata(name="language")
    @property
    def language(self) -> Optional[str]:
        """Gets the language property"""
        return self.properties.get("language", None)

    @odata(name="seller")
    @property
    def seller(self) -> Optional[str]:
        """Gets the seller property"""
        return self.properties.get("seller", None)

    @odata(name="totalLicenseCount")
    @property
    def total_license_count(self) -> Optional[int]:
        """Gets the totalLicenseCount property"""
        return self.properties.get("totalLicenseCount", None)

    @odata(name="usedLicenseCount")
    @property
    def used_license_count(self) -> Optional[int]:
        """Gets the usedLicenseCount property"""
        return self.properties.get("usedLicenseCount", None)

    @odata(name="vppOrganizationName")
    @property
    def vpp_organization_name(self) -> Optional[str]:
        """Gets the vppOrganizationName property"""
        return self.properties.get("vppOrganizationName", None)

    @odata(name="vppTokenId")
    @property
    def vpp_token_id(self) -> Optional[UUID]:
        """Gets the vppTokenId property"""
        return self.properties.get("vppTokenId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IosVppEBook"
