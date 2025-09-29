from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.compliance.classificationpublishconfig import (
    SPClassificationPublishConfig,
)
from office365.sharepoint.contentcenter.machinelearning.extractorpublishconfig import (
    SPExtractorPublishConfig,
)


class SPModelPublishConfig(ClientValue):

    def __init__(
        self,
        classification_publish_configs: ClientValueCollection[
            SPClassificationPublishConfig
        ] = ClientValueCollection(SPClassificationPublishConfig),
        extractor_publish_configs: ClientValueCollection[
            SPExtractorPublishConfig
        ] = ClientValueCollection(SPExtractorPublishConfig),
    ):
        self.ClassificationPublishConfigs = classification_publish_configs
        self.ExtractorPublishConfigs = extractor_publish_configs
