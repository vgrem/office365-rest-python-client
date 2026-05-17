from datetime import datetime

from office365.runtime.client_value import ClientValue
from typing import Optional


class UnlicensedOdbTenantMetrics(ClientValue):
    def __init__(
        self,
        admin_locked_count: Optional[int] = None,
        admin_locked_size_bytes: Optional[float] = None,
        billable_count: Optional[int] = None,
        billable_size_bytes: Optional[float] = None,
        compliance_hold_count: Optional[int] = None,
        compliance_hold_size_bytes: Optional[float] = None,
        count: Optional[int] = None,
        duplicate_site_count: Optional[int] = None,
        duplicate_site_size_bytes: Optional[float] = None,
        invalid_license_count: Optional[int] = None,
        invalid_license_size_bytes: Optional[float] = None,
        last_refresh_on: Optional[datetime] = None,
        restored_by_tenant_admin_count: Optional[int] = None,
        restored_by_tenant_admin_size_bytes: Optional[float] = None,
        retention_period_count: Optional[int] = None,
        retention_period_size_bytes: Optional[float] = None,
        size_bytes: Optional[float] = None,
        unknown_count: Optional[int] = None,
        unknown_size_bytes: Optional[float] = None,
    ):
        self.adminLockedCount = admin_locked_count
        self.adminLockedSizeBytes = admin_locked_size_bytes
        self.billableCount = billable_count
        self.billableSizeBytes = billable_size_bytes
        self.complianceHoldCount = compliance_hold_count
        self.complianceHoldSizeBytes = compliance_hold_size_bytes
        self.count = count
        self.duplicateSiteCount = duplicate_site_count
        self.duplicateSiteSizeBytes = duplicate_site_size_bytes
        self.invalidLicenseCount = invalid_license_count
        self.invalidLicenseSizeBytes = invalid_license_size_bytes
        self.lastRefreshOn = last_refresh_on
        self.restoredByTenantAdminCount = restored_by_tenant_admin_count
        self.restoredByTenantAdminSizeBytes = restored_by_tenant_admin_size_bytes
        self.retentionPeriodCount = retention_period_count
        self.retentionPeriodSizeBytes = retention_period_size_bytes
        self.sizeBytes = size_bytes
        self.unknownCount = unknown_count
        self.unknownSizeBytes = unknown_size_bytes

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.OdbLicenseEnforcement.UnlicensedOdbTenantMetrics"
