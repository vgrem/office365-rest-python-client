from office365.entity import Entity
from office365.partners.billing.billing import Billing
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class Partners(Entity):
    """Represents billing details for a Microsoft direct partner."""

    @odata(name="billing", navigation=True)
    @property
    def billing(self) -> Billing:
        """
        Represents billing details for billed and unbilled data.
        """
        return self.properties.get("billing", Billing(self.context, ResourcePath("billing", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Partners"
