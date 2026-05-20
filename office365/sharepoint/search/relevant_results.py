from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.utilities import parse_key_value_collection
from office365.sharepoint.search.simple_data_table import SimpleDataTable


@dataclass
class RelevantResults(ClientValue):
    """
    The RelevantResults table contains the actual query results. It MUST only be present if the ResultTypes element
    in the properties element of the Execute message contains ResultType.RelevantResults,
    as specified in section 2.2.5.5
    """

    GroupTemplateId: str | None = None
    ItemTemplateId: str | None = None
    Properties: dict = field(default_factory=dict)
    ResultTitle: str | None = None
    ResultTitleUrl: str | None = None
    Table: SimpleDataTable = field(default_factory=SimpleDataTable)
    RowCount: int | None = None
    TotalRows: int | None = None
    TotalRowsIncludingDuplicates: int | None = None

    def set_property(self, k, v, persist_changes=True):
        if k == "Properties":
            v = parse_key_value_collection(v)
        super().set_property(k, v, persist_changes)
        return self

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.RelevantResults"
