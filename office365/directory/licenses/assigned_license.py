from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection

if TYPE_CHECKING:
    from office365.directory.licenses.subscribed_sku import SubscribedSku


class AssignedLicense(ClientValue):
    """
    Represents a license assigned to a user. The assignedLicenses property of the user entity is a collection
    of assignedLicense.
    """

    skuId: str | None = None
    disabledPlans: StringCollection = field(default_factory=StringCollection)

    def __repr__(self):
        return str(self.skuId or "")

    def disabled_plan_names(self, sku: SubscribedSku | None = None) -> list[str]:
        """The disabled plans by name, resolved against the SKU that carries them.

        Args:
            sku (SubscribedSku): The catalogue entry for :attr:`skuId`. Without it — the tenant
                no longer subscribes to the SKU — the ids stand for themselves, since only the
                SKU knows the names.
        """
        if sku is None:
            return [str(plan_id) for plan_id in self.disabledPlans]
        return [sku.plan_name(plan_id) for plan_id in self.disabledPlans]

    @property
    def entity_type_name(self):
        return "microsoft.graph.AssignedLicense"
