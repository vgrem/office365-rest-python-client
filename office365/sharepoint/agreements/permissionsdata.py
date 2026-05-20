from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AgreementPermissionsData(ClientValue):
    can_add_amendment: Optional[bool] = None
    can_create_agreement: Optional[bool] = None
    can_create_template: Optional[bool] = None
    can_import_agreement: Optional[bool] = None
    can_upload_signed_version: Optional[bool] = None
    is_workspace_owner: Optional[bool] = None
