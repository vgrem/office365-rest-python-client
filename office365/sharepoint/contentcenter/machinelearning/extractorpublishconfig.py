from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SPExtractorPublishConfig(ClientValue):
    ColumnInternalName: Optional[str] = None
    ColumnName: Optional[str] = None
    ColumnType: Optional[str] = None
    ExtractorId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPExtractorPublishConfig"
