from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.vpptokens.accounttype import VppTokenAccountType
from office365.intune.devices.management.vpptokens.state import VppTokenState
from office365.intune.devices.management.vpptokens.syncstatus import VppTokenSyncStatus


class VppToken(Entity):
    """
    You purchase multiple licenses for iOS apps through the Apple Volume Purchase Program for Business or Education.
    This involves setting up an Apple VPP account from the Apple website and uploading the Apple VPP Business or
    Education token to Intune. You can then synchronize your volume purchase information with Intune and track your
    volume-purchased app use. You can upload multiple Apple VPP Business or Education tokens.
    """

    @property
    def apple_id(self) -> Optional[str]:
        """Gets the appleId property"""
        return self.properties.get("appleId", None)

    @property
    def automatically_update_apps(self) -> Optional[bool]:
        """Gets the automaticallyUpdateApps property"""
        return self.properties.get("automaticallyUpdateApps", None)

    @property
    def country_or_region(self) -> Optional[str]:
        """Gets the countryOrRegion property"""
        return self.properties.get("countryOrRegion", None)

    @property
    def expiration_date_time(self) -> datetime:
        """Gets the expirationDateTime property"""
        return self.properties.get("expirationDateTime", datetime.min)

    @property
    def last_modified_date_time(self) -> datetime:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @property
    def last_sync_date_time(self) -> datetime:
        """Gets the lastSyncDateTime property"""
        return self.properties.get("lastSyncDateTime", datetime.min)

    @property
    def last_sync_status(self) -> VppTokenSyncStatus:
        """Gets the lastSyncStatus property"""
        return self.properties.get("lastSyncStatus", VppTokenSyncStatus.none)

    @property
    def organization_name(self) -> Optional[str]:
        """Gets the organizationName property"""
        return self.properties.get("organizationName", None)

    @property
    def state(self) -> VppTokenState:
        """Gets the state property"""
        return self.properties.get("state", VppTokenState.unknown)

    @property
    def token(self) -> Optional[str]:
        """Gets the token property"""
        return self.properties.get("token", None)

    @property
    def vpp_token_account_type(self) -> VppTokenAccountType:
        """Gets the vppTokenAccountType property"""
        return self.properties.get("vppTokenAccountType", VppTokenAccountType.business)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VppToken"
