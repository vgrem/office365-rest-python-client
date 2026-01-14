from office365.runtime.client_value import ClientValue


class SyntexCustomModelDeploymentModelInfo(ClientValue):
    def __init__(self, format_: str = None, name: str = None, version: str = None):
        self.format = format_
        self.name = name
        self.version = version
