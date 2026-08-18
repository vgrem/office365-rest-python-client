from datetime import datetime
from typing import Optional

from office365.directory.audit.signins.authentication_app_device_details import AuthenticationAppDeviceDetails
from office365.directory.audit.signins.location import SignInLocation
from office365.directory.audit.signins.status import SignInStatus
from office365.directory.authentication.conditionalaccessstatus import ConditionalAccessStatus
from office365.directory.policies.applied_conditional_access import AppliedConditionalAccessPolicy
from office365.directory.protection.riskyusers.riskeventtype import RiskEventType
from office365.directory.protection.riskyusers.risklevel import RiskLevel
from office365.directory.protection.riskyusers.riskstate import RiskState
from office365.entity import Entity
from office365.intune.devices.detail import DeviceDetail
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class SignIn(Entity):
    """Details user and application sign-in activity for a tenant (directory).
    You must have an Azure AD Premium P1 or P2 license to download sign-in logs using the Microsoft Graph API.
    """

    @property
    def app_display_name(self) -> Optional[str]:
        """App name displayed in the Azure Portal."""
        return self.properties.get("appDisplayName", None)

    @property
    def app_id(self) -> Optional[str]:
        """Unique GUID representing the app ID in the Azure Active Directory."""
        return self.properties.get("appId", None)

    @odata(name="appliedConditionalAccessPolicies")
    @property
    def applied_conditional_access_policies(self) -> Optional[ClientValueCollection[AppliedConditionalAccessPolicy]]:
        """Provides a list of conditional access policies that the corresponding sign-in activity triggers."""
        return self.properties.get(
            "appliedConditionalAccessPolicies", ClientValueCollection(AppliedConditionalAccessPolicy)
        )

    @property
    def client_app_used(self) -> Optional[str]:
        """
        Identifies the client used for the sign-in activity. Modern authentication clients include Browser, modern
        clients. Legacy authentication clients include Exchange ActiveSync, IMAP, MAPI, SMTP, POP, and other clients.
        """
        return self.properties.get("clientAppUsed", None)

    @property
    def correlation_id(self) -> Optional[str]:
        """
        The request ID sent from the client when the sign-in is initiated; used to troubleshoot sign-in activity.
        """
        return self.properties.get("correlationId", None)

    @odata(name="createdDateTime")
    @property
    def created_datetime(self) -> datetime:
        """Date and time (UTC) the sign-in was initiated."""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="deviceDetail")
    @property
    def device_detail(self) -> DeviceDetail:
        """Device information from where the sign-in occurred; includes device ID, operating system, and browser.
        Supports $filter (eq and startsWith operators only) on browser and operatingSytem properties.
        """
        return self.properties.get("deviceDetail", DeviceDetail())

    @property
    def ip_address(self) -> Optional[str]:
        """IP address of the client used to sign in."""
        return self.properties.get("ipAddress", None)

    @property
    def is_interactive(self) -> Optional[bool]:
        """Indicates if a sign-in is interactive or not."""
        return self.properties.get("isInteractive", None)

    @property
    def location(self):
        """
        Provides the city, state, and country code where the sign-in originated.
        Supports $filter (eq and startsWith operators only) on city, state, and countryOrRegion properties.
        """
        return self.properties.get("status", SignInLocation())

    @property
    def resource_display_name(self) -> Optional[str]:
        """Name of the resource the user signed into."""
        return self.properties.get("resourceDisplayName", None)

    @property
    def resource_id(self) -> Optional[str]:
        """
        ID of the resource that the user signed into."""
        return self.properties.get("resourceId", None)

    @property
    def risk_detail(self) -> Optional[str]:
        """
        Provides the 'reason' behind a specific state of a risky user, sign-in or a risk event.
        """
        return self.properties.get("riskDetail", None)

    @property
    def user_display_name(self) -> Optional[str]:
        """
        Display name of the user that initiated the sign-in. Supports $filter (eq operator only).
        """
        return self.properties.get("userDisplayName", None)

    @property
    def user_id(self) -> Optional[str]:
        """
        ID of the user that initiated the sign-in. Supports $filter (eq operator only).
        """
        return self.properties.get("userId", None)

    @property
    def user_principal_name(self) -> Optional[str]:
        """
        User principal name of the user that initiated the sign-in. Supports $filter (eq and startsWith operators only).
        """
        return self.properties.get("userPrincipalName", None)

    @property
    def status(self) -> Optional[SignInStatus]:
        """
        Sign-in status. Includes the error code and description of the error (in case of a sign-in failure).
        Supports $filter (eq operator only) on errorCode property.
        """
        return self.properties.get("status", SignInStatus())

    @property
    def authentication_app_device_details(self) -> AuthenticationAppDeviceDetails:
        """Gets the authenticationAppDeviceDetails property"""
        return self.properties.get("authenticationAppDeviceDetails", AuthenticationAppDeviceDetails())

    @property
    def conditional_access_status(self) -> ConditionalAccessStatus:
        """Gets the conditionalAccessStatus property"""
        return self.properties.get("conditionalAccessStatus", ConditionalAccessStatus.success)

    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def home_tenant_id(self) -> Optional[str]:
        """Gets the homeTenantId property"""
        return self.properties.get("homeTenantId", None)

    @property
    def resource_tenant_id(self) -> Optional[str]:
        """Gets the resourceTenantId property"""
        return self.properties.get("resourceTenantId", None)

    @property
    def risk_event_types(self) -> ClientValueCollection[RiskEventType]:
        """Gets the riskEventTypes property"""
        return self.properties.get("riskEventTypes", ClientValueCollection[RiskEventType](RiskEventType))

    @property
    def risk_event_types_v2(self) -> StringCollection:
        """Gets the riskEventTypes_v2 property"""
        return self.properties.get("riskEventTypes_v2", StringCollection(None))

    @property
    def risk_level_aggregated(self) -> RiskLevel:
        """Gets the riskLevelAggregated property"""
        return self.properties.get("riskLevelAggregated", RiskLevel.low)

    @property
    def risk_level_during_sign_in(self) -> RiskLevel:
        """Gets the riskLevelDuringSignIn property"""
        return self.properties.get("riskLevelDuringSignIn", RiskLevel.low)

    @property
    def risk_state(self) -> RiskState:
        """Gets the riskState property"""
        return self.properties.get("riskState", RiskState.none)

    @property
    def service_principal_id(self) -> Optional[str]:
        """Gets the servicePrincipalId property"""
        return self.properties.get("servicePrincipalId", None)

    @property
    def service_principal_name(self) -> Optional[str]:
        """Gets the servicePrincipalName property"""
        return self.properties.get("servicePrincipalName", None)

    @property
    def user_agent(self) -> Optional[str]:
        """Gets the userAgent property"""
        return self.properties.get("userAgent", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SignIn"
