from office365.runtime.client_value import ClientValue


class PlaceholderV2(ClientValue):

    def __init__(
        self,
        additional_fields_data: str = None,
        column_id: str = None,
        column_internal_name: str = None,
        data_type: str = None,
        field_library_mapped_id: str = None,
        field_library_mapped_version: str = None,
        id_: str = None,
        is_column_mapping_active: bool = None,
        is_mandatory: bool = None,
        name: str = None,
        question_title: str = None,
        source: str = None,
    ):
        self.AdditionalFieldsData = additional_fields_data
        self.ColumnId = column_id
        self.ColumnInternalName = column_internal_name
        self.DataType = data_type
        self.FieldLibraryMappedId = field_library_mapped_id
        self.FieldLibraryMappedVersion = field_library_mapped_version
        self.Id = id_
        self.IsColumnMappingActive = is_column_mapping_active
        self.IsMandatory = is_mandatory
        self.Name = name
        self.QuestionTitle = question_title
        self.Source = source
        self.Id = id_
