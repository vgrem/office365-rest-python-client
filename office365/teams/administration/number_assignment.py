from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.teams.administration.assignment_category import AssignmentCategory


class NumberAssignment(Entity):
    @property
    def assignment_category(self) -> AssignmentCategory:
        """Gets the assignmentCategory property"""
        return self.properties.get("assignmentCategory", AssignmentCategory())

    @property
    def assignment_target_id(self) -> Optional[str]:
        """Gets the assignmentTargetId property"""
        return self.properties.get("assignmentTargetId", None)

    @property
    def city(self) -> Optional[str]:
        """Gets the city property"""
        return self.properties.get("city", None)

    @property
    def civic_address_id(self) -> Optional[str]:
        """Gets the civicAddressId property"""
        return self.properties.get("civicAddressId", None)

    @property
    def iso_country_code(self) -> Optional[str]:
        """Gets the isoCountryCode property"""
        return self.properties.get("isoCountryCode", None)

    @property
    def location_id(self) -> Optional[str]:
        """Gets the locationId property"""
        return self.properties.get("locationId", None)

    @property
    def network_site_id(self) -> Optional[str]:
        """Gets the networkSiteId property"""
        return self.properties.get("networkSiteId", None)

    @property
    def operator_id(self) -> Optional[str]:
        """Gets the operatorId property"""
        return self.properties.get("operatorId", None)

    @property
    def telephone_number(self) -> Optional[str]:
        """Gets the telephoneNumber property"""
        return self.properties.get("telephoneNumber", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.NumberAssignment"
