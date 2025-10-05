from office365.runtime.client_value import ClientValue


class SPExtractorPublishConfig(ClientValue):

    def __init__(
        self,
        column_internal_name: str = None,
        column_name: str = None,
        column_type: str = None,
        extractor_id: str = None,
    ):
        self.ColumnInternalName = column_internal_name
        self.ColumnName = column_name
        self.ColumnType = column_type
        self.ExtractorId = extractor_id

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPExtractorPublishConfig"
