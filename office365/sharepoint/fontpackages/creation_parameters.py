from typing import Optional

from office365.runtime.client_value import ClientValue


class FontPackageCreationParameters(ClientValue):
    def __init__(
        self, is_hidden: Optional[bool] = None, package_json: Optional[str] = None, title: Optional[str] = None
    ):
        self.IsHidden = is_hidden
        self.PackageJson = package_json
        self.Title = title

    ""
