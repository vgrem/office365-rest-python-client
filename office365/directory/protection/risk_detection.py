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


class RiskDetection(Entity):
    """
    Represents information about a detected risk in an Azure AD tenant.

    Azure AD continually evaluates user risks and app or user sign-in risks based on various signals
    and machine learning.
    This API provides programmatic access to all risk detections in your Azure AD environment.
    """

    @property
    def activity(self) -> ActivityType:
        """Gets the activity property"""
        return self.properties.get("activity", ActivityType.signin)

    @property
    def activity_date_time(self) -> datetime:
        """Gets the activityDateTime property"""
        return self.properties.get("activityDateTime", datetime.min)

    @property
    def additional_info(self) -> Optional[str]:
        """Gets the additionalInfo property"""
        return self.properties.get("additionalInfo", None)

    @property
    def correlation_id(self) -> Optional[str]:
        """Gets the correlationId property"""
        return self.properties.get("correlationId", None)

    @property
    def detected_date_time(self) -> datetime:
        """Gets the detectedDateTime property"""
        return self.properties.get("detectedDateTime", datetime.min)

    @property
    def detection_timing_type(self) -> RiskDetectionTimingType:
        """Gets the detectionTimingType property"""
        return self.properties.get("detectionTimingType", RiskDetectionTimingType.notDefined)

    @property
    def ip_address(self) -> Optional[str]:
        """Gets the ipAddress property"""
        return self.properties.get("ipAddress", None)

    @property
    def last_updated_date_time(self) -> datetime:
        """Gets the lastUpdatedDateTime property"""
        return self.properties.get("lastUpdatedDateTime", datetime.min)

    @property
    def location(self) -> SignInLocation:
        """Gets the location property"""
        return self.properties.get("location", SignInLocation())

    @property
    def request_id(self) -> Optional[str]:
        """Gets the requestId property"""
        return self.properties.get("requestId", None)

    @property
    def risk_detail(self) -> RiskDetail:
        """Gets the riskDetail property"""
        return self.properties.get("riskDetail", RiskDetail.none)

    @property
    def risk_event_type(self) -> Optional[str]:
        """Gets the riskEventType property"""
        return self.properties.get("riskEventType", None)

    @property
    def risk_level(self) -> RiskLevel:
        """Gets the riskLevel property"""
        return self.properties.get("riskLevel", RiskLevel.low)

    @property
    def risk_state(self) -> RiskState:
        """Gets the riskState property"""
        return self.properties.get("riskState", RiskState.none)

    @property
    def source(self) -> Optional[str]:
        """Gets the source property"""
        return self.properties.get("source", None)

    @property
    def token_issuer_type(self) -> TokenIssuerType:
        """Gets the tokenIssuerType property"""
        return self.properties.get("tokenIssuerType", TokenIssuerType.AzureAD)

    @property
    def user_display_name(self) -> Optional[str]:
        """Gets the userDisplayName property"""
        return self.properties.get("userDisplayName", None)

    @property
    def user_id(self) -> Optional[str]:
        """Gets the userId property"""
        return self.properties.get("userId", None)

    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the userPrincipalName property"""
        return self.properties.get("userPrincipalName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RiskDetection"
