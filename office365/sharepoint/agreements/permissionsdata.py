from typing import Optional

from office365.runtime.client_value import ClientValue


class AgreementPermissionsData(ClientValue):
    def __init__(
        self,
        can_add_amendment: Optional[bool] = None,
        can_create_agreement: Optional[bool] = None,
        can_create_template: Optional[bool] = None,
        can_import_agreement: Optional[bool] = None,
        can_upload_signed_version: Optional[bool] = None,
        is_workspace_owner: Optional[bool] = None,
    ):
        self.can_add_amendment = can_add_amendment
        self.can_create_agreement = can_create_agreement
        self.can_create_template = can_create_template
        self.can_import_agreement = can_import_agreement
        self.can_upload_signed_version = can_upload_signed_version
        self.is_workspace_owner = is_workspace_owner
