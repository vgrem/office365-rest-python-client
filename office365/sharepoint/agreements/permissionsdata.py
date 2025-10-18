from office365.runtime.client_value import ClientValue


class AgreementPermissionsData(ClientValue):

    def __init__(
        self,
        can_add_amendment: bool = None,
        can_create_agreement: bool = None,
        can_create_template: bool = None,
        can_import_agreement: bool = None,
        can_upload_signed_version: bool = None,
        is_workspace_owner: bool = None,
    ):
        self.can_add_amendment = can_add_amendment
        self.can_create_agreement = can_create_agreement
        self.can_create_template = can_create_template
        self.can_import_agreement = can_import_agreement
        self.can_upload_signed_version = can_upload_signed_version
        self.is_workspace_owner = is_workspace_owner
