from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.files.versions.policyselectionparameters import (
    VersionPolicySelectionParameters,
)


class FileVersionBatchDeleteParameters(ClientValue):
    def __init__(
        self,
        batch_delete_mode: Optional[int] = None,
        delete_older_than_days: Optional[int] = None,
        file_type_selections: VersionPolicySelectionParameters = VersionPolicySelectionParameters(),
        major_version_limit: Optional[int] = None,
        major_with_minor_versions_limit: Optional[int] = None,
        sync_list_policy: Optional[bool] = None,
    ):
        self.batch_delete_mode = batch_delete_mode
        self.delete_older_than_days = delete_older_than_days
        self.file_type_selections = file_type_selections
        self.major_version_limit = major_version_limit
        self.major_with_minor_versions_limit = major_with_minor_versions_limit
        self.sync_list_policy = sync_list_policy
