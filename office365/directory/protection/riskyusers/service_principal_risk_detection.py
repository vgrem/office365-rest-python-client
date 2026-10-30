from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.audit.signins.location import SignInLocation
from office365.directory.protection.activitytype import ActivityType
from office365.directory.protection.riskdetectiontimingtype import RiskDetectionTimingType
from office365.directory.protection.riskyusers.risk_detail import RiskDetail
from office365.directory.protection.riskyusers.risklevel import RiskLevel
from office365.directory.protection.riskyusers.riskstate import RiskState
from office365.directory.protection.tokenissuertype import TokenIssuerType
from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class ServicePrincipalRiskDetection(Entity):
    @odata(name="activity")
    @property
    def activity(self) -> ActivityType:
        """Gets the activity property"""
        return self.properties.get("activity", ActivityType.signin)

    @odata(name="activityDateTime")
    @property
    def activity_date_time(self) -> datetime:
        """Gets the activityDateTime property"""
        return self.properties.get("activityDateTime", datetime.min)

    @odata(name="additionalInfo")
    @property
    def additional_info(self) -> Optional[str]:
        """Gets the additionalInfo property"""
        return self.properties.get("additionalInfo", None)

    @odata(name="appId")
    @property
    def app_id(self) -> Optional[str]:
        """Gets the appId property"""
        return self.properties.get("appId", None)

    @odata(name="correlationId")
    @property
    def correlation_id(self) -> Optional[str]:
        """Gets the correlationId property"""
        return self.properties.get("correlationId", None)

    @odata(name="detectedDateTime")
    @property
    def detected_date_time(self) -> datetime:
        """Gets the detectedDateTime property"""
        return self.properties.get("detectedDateTime", datetime.min)

    @odata(name="detectionTimingType")
    @property
    def detection_timing_type(self) -> RiskDetectionTimingType:
        """Gets the detectionTimingType property"""
        return self.properties.get("detectionTimingType", RiskDetectionTimingType.notDefined)

    @odata(name="ipAddress")
    @property
    def ip_address(self) -> Optional[str]:
        """Gets the ipAddress property"""
        return self.properties.get("ipAddress", None)

    @odata(name="keyIds")
    @property
    def key_ids(self) -> StringCollection:
        """Gets the keyIds property"""
        return self.properties.get("keyIds", StringCollection(None))

    @odata(name="lastUpdatedDateTime")
    @property
    def last_updated_date_time(self) -> datetime:
        """Gets the lastUpdatedDateTime property"""
        return self.properties.get("lastUpdatedDateTime", datetime.min)

    @odata(name="location")
    @property
    def location(self) -> SignInLocation:
        """Gets the location property"""
        return self.properties.get("location", SignInLocation())

    @odata(name="requestId")
    @property
    def request_id(self) -> Optional[str]:
        """Gets the requestId property"""
        return self.properties.get("requestId", None)

    @odata(name="riskDetail")
    @property
    def risk_detail(self) -> RiskDetail:
        """Gets the riskDetail property"""
        return self.properties.get("riskDetail", RiskDetail.none)

    @odata(name="riskEventType")
    @property
    def risk_event_type(self) -> Optional[str]:
        """Gets the riskEventType property"""
        return self.properties.get("riskEventType", None)

    @odata(name="riskLevel")
    @property
    def risk_level(self) -> RiskLevel:
        """Gets the riskLevel property"""
        return self.properties.get("riskLevel", RiskLevel.low)

    @odata(name="riskState")
    @property
    def risk_state(self) -> RiskState:
        """Gets the riskState property"""
        return self.properties.get("riskState", RiskState.none)

    @odata(name="servicePrincipalDisplayName")
    @property
    def service_principal_display_name(self) -> Optional[str]:
        """Gets the servicePrincipalDisplayName property"""
        return self.properties.get("servicePrincipalDisplayName", None)

    @odata(name="servicePrincipalId")
    @property
    def service_principal_id(self) -> Optional[str]:
        """Gets the servicePrincipalId property"""
        return self.properties.get("servicePrincipalId", None)

    @odata(name="source")
    @property
    def source(self) -> Optional[str]:
        """Gets the source property"""
        return self.properties.get("source", None)

    @odata(name="tokenIssuerType")
    @property
    def token_issuer_type(self) -> TokenIssuerType:
        """Gets the tokenIssuerType property"""
        return self.properties.get("tokenIssuerType", TokenIssuerType.AzureAD)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ServicePrincipalRiskDetection"
