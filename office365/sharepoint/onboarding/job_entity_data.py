from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class JobEntityData(Entity):
    """"""

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.Onboarding.RestService.JobEntityData"

    @odata(name="Option")
    @property
    def option(self) -> Optional[int]:
        """Gets the Option property"""
        return self.properties.get("Option", None)

    @odata(name="Reserve")
    @property
    def reserve(self) -> Optional[str]:
        """Gets the Reserve property"""
        return self.properties.get("Reserve", None)
