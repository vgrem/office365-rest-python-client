from office365.runtime.client_value import ClientValue


class FontPackageCreationParameters(ClientValue):

    def __init__(self, is_hidden: bool = None, package_json: str = None, title: str = None):
        self.IsHidden = is_hidden
        self.PackageJson = package_json
        self.Title = title

    ""
