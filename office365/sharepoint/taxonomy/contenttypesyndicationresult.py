from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class ContentTypeSyndicationResult(ClientValue):
    def __init__(
        self,
        failed_content_type_errors: StringCollection = StringCollection(),
        failed_content_type_i_ds: StringCollection = StringCollection(),
        failed_reason: int = None,
        is_passed: bool = None,
    ):
        self.FailedContentTypeErrors = failed_content_type_errors
        self.FailedContentTypeIDs = failed_content_type_i_ds
        self.FailedReason = failed_reason
        self.IsPassed = is_passed

    @property
    def entity_type_name(self):
        return "SP.Taxonomy.ContentTypeSync.ContentTypeSyndicationResult"
