from office365.runtime.client_value import ClientValue


class RelationData(ClientValue):
    def __init__(
        self,
        attribute_data_source: int = None,
        target_object_id: str = None,
        target_object_subtype: int = None,
        target_object_type: int = None,
        value: bytes = None,
        value_json_string: str = None,
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
