from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import GuidCollection, StringCollection


class SPDataGovernanceInsightCreateParameters(ClientValue):
    CountOfUsersMoreThan: int | None = None
    FileSensitivityLabelGUID: str | None = None
    FileSensitivityLabelName: str | None = None
    Name: str | None = None
    Privacy: str | None = None
    ReportEntity: int | None = None
    ReportType: int | None = None
    SiteSensitivityLabelGUID: GuidCollection = field(default_factory=GuidCollection)
    Template: ClientValueCollection = field(default_factory=ClientValueCollection)
    UserEmailList: StringCollection = field(default_factory=StringCollection)
    UserIDList: GuidCollection = field(default_factory=GuidCollection)
    Workload: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDataGovernanceInsightCreateParameters"
