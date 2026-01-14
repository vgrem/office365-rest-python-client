from office365.runtime.client_value import ClientValue


class FolderCollectionAddParameters(ClientValue):
    def __init__(self, ensure_unique_file_name: bool = None, overwrite: bool = None):
        self.ensure_unique_file_name = ensure_unique_file_name
        self.overwrite = overwrite
