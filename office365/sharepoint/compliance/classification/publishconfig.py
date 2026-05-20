from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.compliance.retentionlabelconfig import SPRetentionLabelConfig
from office365.sharepoint.compliance.sensitivitylabels.config import (
    SPSensitivityLabelConfig,
)


@dataclass
class SPClassificationPublishConfig(ClientValue):
    ClassifierId: Optional[str] = None
    ColumnName: Optional[str] = None
    ColumnType: Optional[str] = None
    ContentType: Optional[str] = None
    Kind: Optional[str] = None
    ModelClassification: Optional[str] = None
    ModelId: Optional[str] = None
    RetentionLabel: SPRetentionLabelConfig = field(default_factory=SPRetentionLabelConfig)
    SensitivityLabel: SPSensitivityLabelConfig = field(default_factory=SPSensitivityLabelConfig)

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPClassificationPublishConfig"
