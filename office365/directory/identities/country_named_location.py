from __future__ import annotations

from typing import Optional

from office365.directory.identities.countrylookupmethodtype import CountryLookupMethodType
from office365.entity import Entity
from office365.runtime.types.collections import StringCollection


class CountryNamedLocation(Entity):
    @property
    def countries_and_regions(self) -> StringCollection:
        """Gets the countriesAndRegions property"""
        return self.properties.get("countriesAndRegions", StringCollection(None))

    @property
    def country_lookup_method(self) -> CountryLookupMethodType:
        """Gets the countryLookupMethod property"""
        return self.properties.get("countryLookupMethod", CountryLookupMethodType.clientIpAddress)

    @property
    def include_unknown_countries_and_regions(self) -> Optional[bool]:
        """Gets the includeUnknownCountriesAndRegions property"""
        return self.properties.get("includeUnknownCountriesAndRegions", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CountryNamedLocation"
