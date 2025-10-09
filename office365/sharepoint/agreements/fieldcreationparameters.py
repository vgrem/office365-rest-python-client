from office365.runtime.client_value import ClientValue


class FieldCreationParameters(ClientValue):

    def __init__(
        self,
        data_source: str = None,
        data_type: str = None,
        description: str = None,
        title: str = None,
    ):
        self.DataSource = data_source
        self.DataType = data_type
        self.Description = description
        self.Title = title

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Agreements.Models.FieldCreationParameters"
