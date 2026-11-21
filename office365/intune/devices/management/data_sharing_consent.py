from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.permissions import require_permission, requires_license
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.devices.management.data_sharing_consent import DataSharingConsent


@version("beta")
@requires_license("INTUNE_A")
class DataSharingConsent(Entity):
    @odata(name="grantDateTime")
    @property
    def grant_date_time(self) -> Optional[datetime]:
        """Gets the grantDateTime property"""
        return self.properties.get("grantDateTime", None)

    @odata(name="granted")
    @property
    def granted(self) -> Optional[bool]:
        """Gets the granted property"""
        return self.properties.get("granted", None)

    @odata(name="grantedByUpn")
    @property
    def granted_by_upn(self) -> Optional[str]:
        """Gets the grantedByUpn property"""
        return self.properties.get("grantedByUpn", None)

    @odata(name="grantedByUserId")
    @property
    def granted_by_user_id(self) -> Optional[str]:
        """Gets the grantedByUserId property"""
        return self.properties.get("grantedByUserId", None)

    @odata(name="serviceDisplayName")
    @property
    def service_display_name(self) -> Optional[str]:
        """Gets the serviceDisplayName property"""
        return self.properties.get("serviceDisplayName", None)

    @odata(name="termsUrl")
    @property
    def terms_url(self) -> Optional[str]:
        """Gets the termsUrl property"""
        return self.properties.get("termsUrl", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DataSharingConsent"

    @require_permission(
        delegated=["DeviceManagementServiceConfig.ReadWrite.All"],
        application=["DeviceManagementServiceConfig.ReadWrite.All"],
    )
    def consent_to_data_sharing(self) -> DataSharingConsent:
        """consentToDataSharing operation."""
        from office365.intune.devices.management.data_sharing_consent import DataSharingConsent

        return_type = DataSharingConsent(self.context)
        qry = ServiceOperationQuery(self, "consentToDataSharing", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type
