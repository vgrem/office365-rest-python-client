from typing import Optional

from office365.runtime.client_value import ClientValue


class RelationData(ClientValue):
    def __init__(
        self,
        attribute_data_source: Optional[int] = None,
        target_object_id: Optional[str] = None,
        target_object_subtype: Optional[int] = None,
        target_object_type: Optional[int] = None,
        value: Optional[bytes] = None,
        value_json_string: Optional[str] = None,
    ):
        self.AttributeDataSource = attribute_data_source
        self.TargetObjectId = target_object_id
        self.TargetObjectSubtype = target_object_subtype
        self.TargetObjectType = target_object_type
        self.Value = value
        self.ValueJsonString = value_json_string

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.RelationData"
