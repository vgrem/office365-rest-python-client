from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class ConnectorResult(Entity):
    """ """

    @odata(name="ContextData", beta=True)
    @property
    def context_data(self) -> Optional[str]:
        return self.properties.get("ContextData", None)

    @odata(name="Value", beta=True)
    @property
    def value(self) -> Optional[str]:
        return self.properties.get("Value", None)
