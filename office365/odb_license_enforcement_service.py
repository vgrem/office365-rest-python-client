from __future__ import annotations

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import GuidCollection
from office365.sharepoint.entity import Entity
from office365.sharepoint.tenant.administration.odb_license_updated_user_detail import OdbLicenseUpdatedUserDetail


class OdbLicenseEnforcementService(Entity):
    def process_tenant_odb_license_updated_users(
        self, license_updated_user_details: ClientValueCollection[OdbLicenseUpdatedUserDetail]
    ) -> ClientResult[GuidCollection]:
        """ProcessTenantOdbLicenseUpdatedUsers operation."""
        return_type = ClientResult(self.context, GuidCollection())
        qry = ServiceOperationQuery(
            self,
            "ProcessTenantOdbLicenseUpdatedUsers",
            None,
            {"licenseUpdatedUserDetails": license_updated_user_details},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type
