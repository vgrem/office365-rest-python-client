from typing import Optional

from office365.runtime.client_value import ClientValue


class ColumnDef(ClientValue):
    def __init__(
        self,
        custom_formatter: Optional[str] = None,
        id_: Optional[str] = None,
        name: Optional[str] = None,
        type_: Optional[str] = None,
    ):
        self.CustomFormatter = custom_formatter
        self.Id = id_
        self.Name = name
        self.Type = type_

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.ColumnDef"
