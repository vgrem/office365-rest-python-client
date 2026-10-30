from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.security.average_comparative_score import (
        AverageComparativeScore,
    )
    from office365.security.control_score import ControlScore
    from office365.security.security_vendor_information import (
        SecurityVendorInformation,
    )


class SecureScore(Entity):
    @odata(name="activeUserCount")
    @property
    def active_user_count(self) -> Optional[int]:
        """Gets the activeUserCount property"""
        return self.properties.get("activeUserCount", None)

    @odata(name="averageComparativeScores")
    @property
    def average_comparative_scores(self) -> ClientValueCollection[AverageComparativeScore]:
        """Gets the averageComparativeScores property"""
        from office365.security.average_comparative_score import (
            AverageComparativeScore,
        )

        return self.properties.get(
            "averageComparativeScores", ClientValueCollection[AverageComparativeScore](AverageComparativeScore)
        )

    @odata(name="azureTenantId")
    @property
    def azure_tenant_id(self) -> Optional[str]:
        """Gets the azureTenantId property"""
        return self.properties.get("azureTenantId", None)

    @odata(name="controlScores")
    @property
    def control_scores(self) -> ClientValueCollection[ControlScore]:
        """Gets the controlScores property"""
        from office365.security.control_score import ControlScore

        return self.properties.get("controlScores", ClientValueCollection[ControlScore](ControlScore))

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="currentScore")
    @property
    def current_score(self) -> Optional[float]:
        """Gets the currentScore property"""
        return self.properties.get("currentScore", None)

    @odata(name="enabledServices")
    @property
    def enabled_services(self) -> StringCollection:
        """Gets the enabledServices property"""
        return self.properties.get("enabledServices", StringCollection())

    @odata(name="licensedUserCount")
    @property
    def licensed_user_count(self) -> Optional[int]:
        """Gets the licensedUserCount property"""
        return self.properties.get("licensedUserCount", None)

    @odata(name="maxScore")
    @property
    def max_score(self) -> Optional[float]:
        """Gets the maxScore property"""
        return self.properties.get("maxScore", None)

    @odata(name="vendorInformation")
    @property
    def vendor_information(self) -> SecurityVendorInformation:
        """Gets the vendorInformation property"""
        from office365.security.security_vendor_information import (
            SecurityVendorInformation,
        )

        return self.properties.get("vendorInformation", SecurityVendorInformation())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SecureScore"
