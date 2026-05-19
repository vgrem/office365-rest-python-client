from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.files.versions.policyselectionparameters import (
    VersionPolicySelectionParameters,
)


@dataclass
class FileVersionBatchDeleteParameters(ClientValue):
    batch_delete_mode: int | None = None
    delete_older_than_days: int | None = None
    file_type_selections: VersionPolicySelectionParameters = field(default_factory=VersionPolicySelectionParameters)
    major_version_limit: int | None = None
    major_with_minor_versions_limit: int | None = None
    sync_list_policy: bool | None = None
