from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.compliance.retentionlabelconfig import SPRetentionLabelConfig
from office365.sharepoint.compliance.sensitivitylabels.config import (
    SPSensitivityLabelConfig,
)


class SPClassificationPublishConfig(ClientValue):
    def __init__(
        self,
        classifier_id: Optional[str] = None,
        column_name: Optional[str] = None,
        column_type: Optional[str] = None,
        content_type: Optional[str] = None,
        kind: Optional[str] = None,
        model_classification: Optional[str] = None,
        model_id: Optional[str] = None,
        retention_label: SPRetentionLabelConfig = SPRetentionLabelConfig(),
        sensitivity_label: SPSensitivityLabelConfig = SPSensitivityLabelConfig(),
    ):
        self.ClassifierId = classifier_id
        self.ColumnName = column_name
        self.ColumnType = column_type
        self.ContentType = content_type
        self.Kind = kind
        self.ModelClassification = model_classification
        self.ModelId = model_id
        self.RetentionLabel = retention_label
        self.SensitivityLabel = sensitivity_label

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPClassificationPublishConfig"
