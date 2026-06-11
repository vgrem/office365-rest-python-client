from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AgreementPermissionsData(ClientValue):
    CanAddAmendment: bool | None = None
    CanCreateAgreement: bool | None = None
    CanCreateTemplate: bool | None = None
    CanImportAgreement: bool | None = None
    CanUploadSignedVersion: bool | None = None
    IsWorkspaceOwner: bool | None = None
