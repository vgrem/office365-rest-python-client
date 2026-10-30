from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.security.attacksimulations.payloadbrand import PayloadBrand
from office365.security.attacksimulations.payloadcomplexity import PayloadComplexity
from office365.security.attacksimulations.payloaddeliveryplatform import PayloadDeliveryPlatform
from office365.security.attacksimulations.payloadindustry import PayloadIndustry
from office365.security.attacksimulations.payloadtheme import PayloadTheme
from office365.security.attacksimulations.simulationattacktechnique import SimulationAttackTechnique
from office365.security.attacksimulations.simulationattacktype import SimulationAttackType
from office365.security.attacksimulations.simulationcontentsource import SimulationContentSource
from office365.security.attacksimulations.simulationcontentstatus import SimulationContentStatus

if TYPE_CHECKING:
    from office365.directory.permissions.email_identity import EmailIdentity
    from office365.security.payload_detail import PayloadDetail


class Payload(Entity):
    @odata(name="brand")
    @property
    def brand(self) -> PayloadBrand:
        """Gets the brand property"""
        return self.properties.get("brand", PayloadBrand.unknown)

    @odata(name="complexity")
    @property
    def complexity(self) -> PayloadComplexity:
        """Gets the complexity property"""
        return self.properties.get("complexity", PayloadComplexity.unknown)

    @odata(name="createdBy")
    @property
    def created_by(self) -> EmailIdentity:
        """Gets the createdBy property"""
        from office365.directory.permissions.email_identity import EmailIdentity

        return self.properties.get("createdBy", EmailIdentity())

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="detail")
    @property
    def detail(self) -> PayloadDetail:
        """Gets the detail property"""
        from office365.security.payload_detail import PayloadDetail

        return self.properties.get("detail", PayloadDetail())

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="industry")
    @property
    def industry(self) -> PayloadIndustry:
        """Gets the industry property"""
        return self.properties.get("industry", PayloadIndustry.unknown)

    @odata(name="isAutomated")
    @property
    def is_automated(self) -> Optional[bool]:
        """Gets the isAutomated property"""
        return self.properties.get("isAutomated", None)

    @odata(name="isControversial")
    @property
    def is_controversial(self) -> Optional[bool]:
        """Gets the isControversial property"""
        return self.properties.get("isControversial", None)

    @odata(name="isCurrentEvent")
    @property
    def is_current_event(self) -> Optional[bool]:
        """Gets the isCurrentEvent property"""
        return self.properties.get("isCurrentEvent", None)

    @odata(name="language")
    @property
    def language(self) -> Optional[str]:
        """Gets the language property"""
        return self.properties.get("language", None)

    @odata(name="lastModifiedBy")
    @property
    def last_modified_by(self) -> EmailIdentity:
        """Gets the lastModifiedBy property"""
        from office365.directory.permissions.email_identity import EmailIdentity

        return self.properties.get("lastModifiedBy", EmailIdentity())

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="payloadTags")
    @property
    def payload_tags(self) -> StringCollection:
        """Gets the payloadTags property"""
        return self.properties.get("payloadTags", StringCollection())

    @odata(name="platform")
    @property
    def platform(self) -> PayloadDeliveryPlatform:
        """Gets the platform property"""
        return self.properties.get("platform", PayloadDeliveryPlatform.unknown)

    @odata(name="predictedCompromiseRate")
    @property
    def predicted_compromise_rate(self) -> Optional[float]:
        """Gets the predictedCompromiseRate property"""
        return self.properties.get("predictedCompromiseRate", None)

    @odata(name="simulationAttackType")
    @property
    def simulation_attack_type(self) -> SimulationAttackType:
        """Gets the simulationAttackType property"""
        return self.properties.get("simulationAttackType", SimulationAttackType.unknown)

    @odata(name="source")
    @property
    def source(self) -> SimulationContentSource:
        """Gets the source property"""
        return self.properties.get("source", SimulationContentSource.unknown)

    @odata(name="status")
    @property
    def status(self) -> SimulationContentStatus:
        """Gets the status property"""
        return self.properties.get("status", SimulationContentStatus.unknown)

    @odata(name="technique")
    @property
    def technique(self) -> SimulationAttackTechnique:
        """Gets the technique property"""
        return self.properties.get("technique", SimulationAttackTechnique.unknown)

    @odata(name="theme")
    @property
    def theme(self) -> PayloadTheme:
        """Gets the theme property"""
        return self.properties.get("theme", PayloadTheme.unknown)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Payload"
