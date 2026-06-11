from typing import Optional

from office365.directory.licenses.service_plan_info import ServicePlanInfo
from office365.directory.licenses.units_detail import LicenseUnitsDetail
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class SubscribedSku(Entity):
    """Contains information about a service SKU that a company is subscribed to."""

    def __str__(self) -> str:
        return self.sku_part_number or self.entity_type_name

    @property
    def account_id(self) -> Optional[str]:
        """The unique ID of the account this SKU belongs to."""
        return self.properties.get("accountId", None)

    @odata(name="accountName")
    @property
    def account_name(self) -> Optional[str]:
        """The name of the account this SKU belongs to."""
        return self.properties.get("accountName", None)

    @property
    def applies_to(self) -> Optional[str]:
        """
        The target class for this SKU. Only SKUs with target class User are assignable.
        Possible values are: "User", "Company".
        """
        return self.properties.get("appliesTo", None)

    @odata(name="capabilityStatus")
    @property
    def capability_status(self) -> Optional[str]:
        """The status of the capability. Possible values: Enabled, Warning, Suspended, Deleted, LockedOut."""
        return self.properties.get("capabilityStatus", None)

    @odata(name="consumedUnits")
    @property
    def consumed_units(self) -> Optional[int]:
        """The number of licenses that have been assigned."""
        return self.properties.get("consumedUnits", None)

    @property
    def sku_id(self) -> Optional[str]:
        """The unique identifier (GUID) for the service SKU."""
        return self.properties.get("skuId", None)

    @property
    def sku_part_number(self) -> Optional[str]:
        """
        The SKU part number; for example: "AAD_PREMIUM" or "RMSBASIC".
        To get a list of commercial subscriptions that an organization has acquired, see List subscribedSkus.
        """
        return self.properties.get("skuPartNumber", None)

    @odata(name="prepaidUnits")
    @property
    def prepaid_units(self) -> LicenseUnitsDetail:
        """Information about the number and status of prepaid licenses."""
        return self.properties.get("prepaidUnits", LicenseUnitsDetail())

    @odata(name="servicePlans")
    @property
    def service_plans(self) -> ClientValueCollection[ServicePlanInfo]:
        """Information about the service plans that are available with the SKU. Not nullable"""
        return self.properties.get("servicePlans", ClientValueCollection(ServicePlanInfo))

    @odata(name="subscriptionIds")
    @property
    def subscription_ids(self) -> StringCollection:
        """The IDs of the subscriptions associated with this SKU."""
        return self.properties.get("subscriptionIds", StringCollection())
