from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.fields.lookup_value import FieldLookupValue


@dataclass
class ListItemFormUpdateValue(ClientValue):
    """Specifies the properties of a list item field and its value.

    :param str name: Specifies the field internal name for a field.
    :param str value: Specifies a value for a field.
    :param bool has_exception: Specifies whether there was an error result after validating the value for the field
    param int ErrorCode: Specifies the error code after validating the value for the field
    """

    FieldName: str | None = None
    FieldValue: str | None = None
    HasException: bool | None = None
    ErrorCode: int | None = None
    ErrorMessage: str | None = None
    ItemId: int | None = None

    def __repr__(self):
        if self.HasException:
            return f"{self.FieldName} update failed: Message: {self.ErrorMessage}"
        else:
            return f"{self.FieldName} update succeeded"

    def to_json(self, json_format=None):
        json = super().to_json(json_format)
        if isinstance(self.FieldValue, FieldLookupValue):
            json["FieldValue"] = "[{" + f"'Key':'{self.FieldValue.LookupValue}'" + "}]"
        elif isinstance(self.FieldValue, datetime):
            json["FieldValue"] = self.FieldValue.isoformat()
        return json

    @property
    def entity_type_name(self):
        return "SP.ListItemFormUpdateValue"
