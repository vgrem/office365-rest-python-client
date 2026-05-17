from office365.runtime.client_value import ClientValue
from typing import Optional


class CustomFontsResource(ClientValue):
    def __init__(
        self,
        byte_array: Optional[bytes] = None,
        file_name: Optional[str] = None,
        full_path: Optional[str] = None,
        maj_ver: Optional[int] = None,
        type_: Optional[int] = None,
    ):
        self.byteArray = byte_array
        self.fileName = file_name
        self.fullPath = full_path
        self.MajVer = maj_ver
        self.type = type_

    " "

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.CustomFontsResource"
