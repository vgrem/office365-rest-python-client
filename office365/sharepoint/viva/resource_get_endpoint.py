from __future__ import annotations

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.viva.resource_link import VivaResourceLink


class VivaResourceGetEndpoint(Entity):
    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.VivaResourceGetEndpoint"

    @odata(name="CompanyLinks")
    @property
    def company_links(self) -> ClientValueCollection[VivaResourceLink]:
        """Gets the CompanyLinks property"""
        return self.properties.get("CompanyLinks", ClientValueCollection[VivaResourceLink](VivaResourceLink))
