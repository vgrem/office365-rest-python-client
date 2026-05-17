from typing import Optional

from office365.runtime.client_value import ClientValue


class FileCollectionAddParameters(ClientValue):
    def __init__(
        self,
        auto_checkout_on_invalid_data: Optional[bool] = None,
        ensure_unique_file_name: Optional[bool] = None,
        overwrite: Optional[bool] = None,
        xor_hash: Optional[str] = None,
    ):
        self.auto_checkout_on_invalid_data = auto_checkout_on_invalid_data
        self.ensure_unique_file_name = ensure_unique_file_name
        self.overwrite = overwrite
        self.xor_hash = xor_hash
