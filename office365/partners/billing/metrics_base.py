from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class BillingMetricsBase(Entity):
    @odata(name="foreignAssociatedTenantBillingManagementActiveCount")
    @property
    def foreign_associated_tenant_billing_management_active_count(self) -> Optional[float]:
        """Gets the foreignAssociatedTenantBillingManagementActiveCount property"""
        return self.properties.get("foreignAssociatedTenantBillingManagementActiveCount", None)

    @odata(name="foreignAssociatedTenantCount")
    @property
    def foreign_associated_tenant_count(self) -> Optional[float]:
        """Gets the foreignAssociatedTenantCount property"""
        return self.properties.get("foreignAssociatedTenantCount", None)

    @odata(name="foreignAssociatedTenantProvisioningActiveCount")
    @property
    def foreign_associated_tenant_provisioning_active_count(self) -> Optional[float]:
        """Gets the foreignAssociatedTenantProvisioningActiveCount property"""
        return self.properties.get("foreignAssociatedTenantProvisioningActiveCount", None)

    @odata(name="localAssociatedTenantBillingManagementActiveCount")
    @property
    def local_associated_tenant_billing_management_active_count(self) -> Optional[float]:
        """Gets the localAssociatedTenantBillingManagementActiveCount property"""
        return self.properties.get("localAssociatedTenantBillingManagementActiveCount", None)

    @odata(name="localAssociatedTenantCount")
    @property
    def local_associated_tenant_count(self) -> Optional[float]:
        """Gets the localAssociatedTenantCount property"""
        return self.properties.get("localAssociatedTenantCount", None)

    @odata(name="localAssociatedTenantIds")
    @property
    def local_associated_tenant_ids(self) -> StringCollection:
        """Gets the localAssociatedTenantIds property"""
        return self.properties.get("localAssociatedTenantIds", StringCollection())

    @odata(name="localAssociatedTenantProvisioningActiveCount")
    @property
    def local_associated_tenant_provisioning_active_count(self) -> Optional[float]:
        """Gets the localAssociatedTenantProvisioningActiveCount property"""
        return self.properties.get("localAssociatedTenantProvisioningActiveCount", None)

    @odata(name="watermarkDateTime")
    @property
    def watermark_date_time(self) -> Optional[datetime]:
        """Gets the watermarkDateTime property"""
        return self.properties.get("watermarkDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BillingMetricsBase"
