from enum import Enum


class SynchronizationMetadata(Enum):
    GalleryApplicationIdentifier = "0"
    GalleryApplicationKey = "1"
    IsOAuthEnabled = "2"
    IsSynchronizationAgentAssignmentRequired = "3"
    IsSynchronizationAgentRequired = "4"
    IsSynchronizationInPreview = "5"
    OAuthSettings = "6"
    SynchronizationLearnMoreIbizaFwLink = "7"
    ConfigurationFields = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SynchronizationMetadata"
