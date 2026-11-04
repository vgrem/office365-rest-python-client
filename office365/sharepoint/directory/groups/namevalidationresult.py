from __future__ import annotations

from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.sharepoint.directory.groups.namevalidationresulterrorparams import (
    GroupNameValidationResultErrorParams,
)


@value
class GroupNameValidationResult(ClientValue):
    AliasErrorDetails: GroupNameValidationResultErrorParams = field(default_factory=GroupNameValidationResultErrorParams)
    DisplayNameErrorDetails: GroupNameValidationResultErrorParams = field(
        default_factory=GroupNameValidationResultErrorParams
    )
    ErrorCode: Optional[str] = None
    ErrorMessage: Optional[str] = None
    IsValidName: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.Directory.GroupNameValidationResult"
