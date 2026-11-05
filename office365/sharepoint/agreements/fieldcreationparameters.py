from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class FieldCreationParameters(ClientValue):
    DataSource: Optional[str] = None
    DataType: Optional[str] = None
    Description: Optional[str] = None
    Title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Agreements.Models.FieldCreationParameters"
