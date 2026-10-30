from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.licenses.service_plan_info import ServicePlanInfo


class CompanySubscription(Entity):
    """Represents a commercial subscription for a tenant. Use the values of skuId and serviceStatus > servicePlanId
    to assign licenses to unassigned users and groups through the user: assignLicense and group: assignLicense
    APIs respectively."""

    @odata(name="commerceSubscriptionId")
    @property
    def commerce_subscription_id(self) -> Optional[str]:
        """Gets the commerceSubscriptionId property"""
        return self.properties.get("commerceSubscriptionId", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="isTrial")
    @property
    def is_trial(self) -> Optional[bool]:
        """Gets the isTrial property"""
        return self.properties.get("isTrial", None)

    @odata(name="nextLifecycleDateTime")
    @property
    def next_lifecycle_date_time(self) -> Optional[datetime]:
        """Gets the nextLifecycleDateTime property"""
        return self.properties.get("nextLifecycleDateTime", datetime.min)

    @odata(name="ownerId")
    @property
    def owner_id(self) -> Optional[str]:
        """Gets the ownerId property"""
        return self.properties.get("ownerId", None)

    @odata(name="ownerTenantId")
    @property
    def owner_tenant_id(self) -> Optional[str]:
        """Gets the ownerTenantId property"""
        return self.properties.get("ownerTenantId", None)

    @odata(name="ownerType")
    @property
    def owner_type(self) -> Optional[str]:
        """Gets the ownerType property"""
        return self.properties.get("ownerType", None)

    @odata(name="serviceStatus")
    @property
    def service_status(self) -> ClientValueCollection[ServicePlanInfo]:
        """Gets the serviceStatus property"""
        from office365.directory.licenses.service_plan_info import ServicePlanInfo

        return self.properties.get("serviceStatus", ClientValueCollection[ServicePlanInfo](ServicePlanInfo))

    @odata(name="skuId")
    @property
    def sku_id(self) -> Optional[str]:
        """Gets the skuId property"""
        return self.properties.get("skuId", None)

    @odata(name="skuPartNumber")
    @property
    def sku_part_number(self) -> Optional[str]:
        """Gets the skuPartNumber property"""
        return self.properties.get("skuPartNumber", None)

    @odata(name="status")
    @property
    def status(self) -> Optional[str]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @odata(name="totalLicenses")
    @property
    def total_licenses(self) -> Optional[int]:
        """Gets the totalLicenses property"""
        return self.properties.get("totalLicenses", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CompanySubscription"
