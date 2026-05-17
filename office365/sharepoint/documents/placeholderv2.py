from office365.runtime.client_value import ClientValue
from typing import Optional


class PlaceholderV2(ClientValue):
    def __init__(
        self,
        additional_fields_data: Optional[str] = None,
        column_id: Optional[str] = None,
        column_internal_name: Optional[str] = None,
        data_type: Optional[str] = None,
        field_library_mapped_id: Optional[str] = None,
        field_library_mapped_version: Optional[str] = None,
        id_: Optional[str] = None,
        is_column_mapping_active: Optional[bool] = None,
        is_mandatory: Optional[bool] = None,
        name: Optional[str] = None,
        question_title: Optional[str] = None,
        source: Optional[str] = None,
    ):
        self.AdditionalFieldsData = additional_fields_data
        self.ColumnId = column_id
        self.ColumnInternalName = column_internal_name
        self.DataType = data_type
        self.FieldLibraryMappedId = field_library_mapped_id
        self.FieldLibraryMappedVersion = field_library_mapped_version
        self.IsColumnMappingActive = is_column_mapping_active
        self.IsMandatory = is_mandatory
        self.Name = name
        self.QuestionTitle = question_title
        self.Source = source
        self.Id = id_
