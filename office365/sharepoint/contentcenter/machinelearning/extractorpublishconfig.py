from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SPExtractorPublishConfig(ClientValue):
    ColumnInternalName: Optional[str] = None
    ColumnName: Optional[str] = None
    ColumnType: Optional[str] = None
    ExtractorId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPExtractorPublishConfig"
