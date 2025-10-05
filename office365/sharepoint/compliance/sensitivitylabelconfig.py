from office365.runtime.client_value import ClientValue


class SPSensitivityLabelConfig(ClientValue):

    def __init__(self, id_: str = None, name: str = None):
        self.Id = id_
        self.Name = name

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPSensitivityLabelConfig"
