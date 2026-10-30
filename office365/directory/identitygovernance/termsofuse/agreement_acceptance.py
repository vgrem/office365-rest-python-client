from datetime import datetime
from typing import Optional

from office365.directory.identitygovernance.termsofuse.agreementacceptancestate import AgreementAcceptanceState
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class AgreementAcceptance(Entity):
    """
    Represents the current status of a user's response to a company's customizable terms of use agreement powered by
    Azure Active Directory (Azure AD).
    """

    @odata(name="agreementFileId")
    @property
    def agreement_file_id(self) -> Optional[str]:
        """The identifier of the agreement file accepted by the user."""
        return self.properties.get("agreementFileId", None)

    @odata(name="agreementId")
    @property
    def agreement_id(self) -> Optional[str]:
        """The identifier of the agreement."""
        return self.properties.get("agreementId", None)

    @odata(name="userPrincipalName")
    @property
    def user_principal_name(self) -> Optional[str]:
        """UPN of the user when the acceptance was recorded."""
        return self.properties.get("userPrincipalName", None)

    @odata(name="deviceDisplayName")
    @property
    def device_display_name(self) -> Optional[str]:
        """Gets the deviceDisplayName property"""
        return self.properties.get("deviceDisplayName", None)

    @odata(name="deviceId")
    @property
    def device_id(self) -> Optional[str]:
        """Gets the deviceId property"""
        return self.properties.get("deviceId", None)

    @odata(name="deviceOSType")
    @property
    def device_os_type(self) -> Optional[str]:
        """Gets the deviceOSType property"""
        return self.properties.get("deviceOSType", None)

    @odata(name="deviceOSVersion")
    @property
    def device_os_version(self) -> Optional[str]:
        """Gets the deviceOSVersion property"""
        return self.properties.get("deviceOSVersion", None)

    @odata(name="expirationDateTime")
    @property
    def expiration_date_time(self) -> datetime:
        """Gets the expirationDateTime property"""
        return self.properties.get("expirationDateTime", datetime.min)

    @odata(name="recordedDateTime")
    @property
    def recorded_date_time(self) -> datetime:
        """Gets the recordedDateTime property"""
        return self.properties.get("recordedDateTime", datetime.min)

    @odata(name="state")
    @property
    def state(self) -> AgreementAcceptanceState:
        """Gets the state property"""
        return self.properties.get("state", AgreementAcceptanceState.accepted)

    @odata(name="userDisplayName")
    @property
    def user_display_name(self) -> Optional[str]:
        """Gets the userDisplayName property"""
        return self.properties.get("userDisplayName", None)

    @odata(name="userEmail")
    @property
    def user_email(self) -> Optional[str]:
        """Gets the userEmail property"""
        return self.properties.get("userEmail", None)

    @odata(name="userId")
    @property
    def user_id(self) -> Optional[str]:
        """Gets the userId property"""
        return self.properties.get("userId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AgreementAcceptance"
