from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.compliance.classification.publishconfig import (
    SPClassificationPublishConfig,
)
from office365.sharepoint.contentcenter.machinelearning.extractorpublishconfig import (
    SPExtractorPublishConfig,
)


@dataclass
class SPModelPublishConfig(ClientValue):
    ClassificationPublishConfigs: ClientValueCollection[SPClassificationPublishConfig] = field(
        default_factory=lambda: ClientValueCollection(SPClassificationPublishConfig)
    )
    ExtractorPublishConfigs: ClientValueCollection[SPExtractorPublishConfig] = field(
        default_factory=lambda: ClientValueCollection(SPExtractorPublishConfig)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPModelPublishConfig"
