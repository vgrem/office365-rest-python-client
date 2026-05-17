from typing import Optional

from office365.runtime.client_value import ClientValue


class FolderCollectionAddParameters(ClientValue):
    def __init__(self, ensure_unique_file_name: Optional[bool] = None, overwrite: Optional[bool] = None):
        self.ensure_unique_file_name = ensure_unique_file_name
        self.overwrite = overwrite
