from office365.runtime.client_value import ClientValue


class SchemaData(ClientValue):

    def __init__(
        self,
        attribute_data_source: int = None,
        delay_load: bool = None,
        is_initialized: bool = None,
        name: str = None,
        privacy: int = None,
    ):
        self.AttributeDataSource = attribute_data_source
        self.DelayLoad = delay_load
        self.IsInitialized = is_initialized
        self.Name = name
        self.Privacy = privacy

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.SchemaData"
