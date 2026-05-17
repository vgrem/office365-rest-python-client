from office365.runtime.client_value import ClientValue
from typing import Optional


class SchemaData(ClientValue):
    def __init__(
        self,
        attribute_data_source: Optional[int] = None,
        delay_load: Optional[bool] = None,
        is_initialized: Optional[bool] = None,
        name: Optional[str] = None,
        privacy: Optional[int] = None,
    ):
        self.AttributeDataSource = attribute_data_source
        self.DelayLoad = delay_load
        self.IsInitialized = is_initialized
        self.Name = name
        self.Privacy = privacy

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.SchemaData"
