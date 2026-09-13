from __future__ import annotations

from typing import Optional

from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.entity import Entity
from office365.sharepoint.multigeo.service.common_move_job import CommonMoveJob


class MoveJobReport(Entity):
    @property
    def jobs(self) -> ClientValueCollection[CommonMoveJob]:
        """Gets the Jobs property"""
        return self.properties.get("Jobs", ClientValueCollection[CommonMoveJob](CommonMoveJob))

    @property
    def report_url(self) -> Optional[str]:
        """Gets the ReportUrl property"""
        return self.properties.get("ReportUrl", None)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.MultiGeo.Service.MoveJobReport"
