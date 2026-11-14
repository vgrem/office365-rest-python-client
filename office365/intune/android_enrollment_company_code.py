from __future__ import annotations

from dataclasses import field

from office365.common.mime_content import MimeContent
from office365.runtime.client_value import ClientValue


class AndroidEnrollmentCompanyCode(ClientValue):
    enrollmentToken: str | None = None
    qrCodeContent: str | None = None
    qrCodeImage: MimeContent = field(default_factory=MimeContent)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AndroidEnrollmentCompanyCode"
