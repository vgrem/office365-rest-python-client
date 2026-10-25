from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class PartnerCompanyIdLookup(Entity):
    @odata(name="PartnerCompanyId")
    @property
    def partner_company_id(self) -> Optional[UUID]:
        """Gets the PartnerCompanyId property"""
        return self.properties.get("PartnerCompanyId", None)

    @odata(name="Result")
    @property
    def result(self) -> Optional[str]:
        """Gets the Result property"""
        return self.properties.get("Result", None)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.MultiGeo.Service.PartnerCompanyIdLookup"
