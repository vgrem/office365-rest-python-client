from office365.runtime.client_value import ClientValue


class CustomFontsResource(ClientValue):

    def __init__(
        self,
        byte_array: bytes = None,
        file_name: str = None,
        full_path: str = None,
        maj_ver: int = None,
        type_: int = None,
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
