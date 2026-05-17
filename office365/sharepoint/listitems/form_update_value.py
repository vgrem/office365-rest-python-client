from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.fields.lookup_value import FieldLookupValue
from typing import Optional


class ListItemFormUpdateValue(ClientValue):
    """Specifies the properties of a list item field and its value."""

    def __init__(
        self,
        name: Optional[str] = None,
        value: Optional[str] = None,
        has_exception: Optional[bool] = None,
        error_code: Optional[int] = None,
        error_message: Optional[str] = None,
        field_name: Optional[str] = None,
        field_value: Optional[str] = None,
        item_id: Optional[int] = None,
    ):
        """
        :param str name: Specifies the field internal name for a field.
        :param str value: Specifies a value for a field.
        :param bool has_exception: Specifies whether there was an error result after validating the value for the field
        param int ErrorCode: Specifies the error code after validating the value for the field
        """
        super().__init__()
        self.FieldName = name
        self.FieldValue = value
        self.HasException = has_exception
        self.ErrorCode = error_code
        self.ErrorMessage = error_message
        self.FieldName = field_name
        self.FieldValue = field_value
        self.ItemId = item_id

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
