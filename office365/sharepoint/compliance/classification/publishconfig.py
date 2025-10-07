from office365.runtime.client_value import ClientValue
from office365.sharepoint.compliance.retentionlabelconfig import SPRetentionLabelConfig
from office365.sharepoint.compliance.sensitivitylabelconfig import (
    SPSensitivityLabelConfig,
)


class SPClassificationPublishConfig(ClientValue):

    def __init__(
        self,
        classifier_id: str = None,
        column_name: str = None,
        column_type: str = None,
        content_type: str = None,
        kind: str = None,
        model_classification: str = None,
        model_id: str = None,
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
