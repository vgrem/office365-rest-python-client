from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.search.simple_data_table import SimpleDataTable


@dataclass
class CustomResult(ClientValue):
    """
    This contains a list of query results, all of which are of the type specified in TableType.
    """

    GroupTemplateId: str | None = None
    ItemTemplateId: str | None = None
    Properties: dict | None = None
    ResultTitle: str | None = None
    ResultTitleUrl: str | None = None
    Table: SimpleDataTable = field(default_factory=SimpleDataTable)
    TableType: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.CustomResult"
