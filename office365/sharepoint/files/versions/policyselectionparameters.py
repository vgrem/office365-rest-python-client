from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class VersionPolicySelectionParameters(ClientValue):
    def __init__(
        self,
        file_types_selected: StringCollection = StringCollection(),
        select_all_file_types: bool = None,
        select_default: bool = None,
    ):
        self.FileTypesSelected = file_types_selected
        self.SelectAllFileTypes = select_all_file_types
        self.SelectDefault = select_default
