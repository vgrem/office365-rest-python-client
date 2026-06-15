from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.tenant.administration.copilot.base_raw_data_sources import BaseRawDataSources
from office365.sharepoint.tenant.administration.copilot.reportrow import ReportRow


class ReportDetails(BaseRawDataSources):
    """ """

    Headers: StringCollection = field(default_factory=StringCollection)
    ReportDownloadUrl: str | None = None
    ReportRows: ClientValueCollection[ReportRow] = field(default_factory=lambda: ClientValueCollection(ReportRow))

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.ReportDetails"
