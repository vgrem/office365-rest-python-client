from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.teams.schedule.eligibilityfilteringenabledentities import (
        EligibilityFilteringEnabledEntities,
    )
    from office365.teams.teamwork.workforce_integration_supported_entities import (
        WorkforceIntegrationSupportedEntities,
    )
    from office365.teams.workforce_integration_encryption import (
        WorkforceIntegrationEncryption,
    )


class WorkforceIntegration(Entity):
    @odata(name="apiVersion")
    @property
    def api_version(self) -> Optional[int]:
        """Gets the apiVersion property"""
        return self.properties.get("apiVersion", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="eligibilityFilteringEnabledEntities")
    @property
    def eligibility_filtering_enabled_entities(self) -> EligibilityFilteringEnabledEntities:
        """Gets the eligibilityFilteringEnabledEntities property"""
        from office365.teams.schedule.eligibilityfilteringenabledentities import (
            EligibilityFilteringEnabledEntities,
        )

        return self.properties.get("eligibilityFilteringEnabledEntities", EligibilityFilteringEnabledEntities.none)

    @odata(name="encryption")
    @property
    def encryption(self) -> WorkforceIntegrationEncryption:
        """Gets the encryption property"""
        from office365.teams.workforce_integration_encryption import (
            WorkforceIntegrationEncryption,
        )

        return self.properties.get("encryption", WorkforceIntegrationEncryption())

    @odata(name="isActive")
    @property
    def is_active(self) -> Optional[bool]:
        """Gets the isActive property"""
        return self.properties.get("isActive", None)

    @odata(name="supportedEntities")
    @property
    def supported_entities(self) -> WorkforceIntegrationSupportedEntities:
        """Gets the supportedEntities property"""
        from office365.teams.teamwork.workforce_integration_supported_entities import (
            WorkforceIntegrationSupportedEntities,
        )

        return self.properties.get("supportedEntities", WorkforceIntegrationSupportedEntities.none)

    @odata(name="url")
    @property
    def url(self) -> Optional[str]:
        """Gets the url property"""
        return self.properties.get("url", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkforceIntegration"
