from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.directory.protection.threatassessment.requests.request import (
    ThreatAssessmentRequest,
)
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.protection.threatassessment.requests.maildestinationroutingreason import (
        MailDestinationRoutingReason,
    )


class EmailFileAssessmentRequest(ThreatAssessmentRequest):
    """
    Represents a resource that creates and retrieves an email file threat assessment.
    The email file can be an .eml file type.
    """

    @odata(name="contentData")
    @property
    def content_data(self) -> Optional[str]:
        """
        Base64 encoded .eml email file content. The file content can't fetch back because it isn't stored.
        """
        return self.properties.get("contentData", None)

    @property
    def file_name(self) -> Optional[str]:
        """
        Base64 encoded .eml email file content. The file content can't fetch back because it isn't stored.
        """
        return self.properties.get("fileName", None)

    @odata(name="destinationRoutingReason")
    @property
    def destination_routing_reason(self) -> MailDestinationRoutingReason:
        """Gets the destinationRoutingReason property"""
        from office365.directory.protection.threatassessment.requests.maildestinationroutingreason import (
            MailDestinationRoutingReason,
        )

        return self.properties.get("destinationRoutingReason", MailDestinationRoutingReason.none)

    @odata(name="recipientEmail")
    @property
    def recipient_email(self) -> Optional[str]:
        """Gets the recipientEmail property"""
        return self.properties.get("recipientEmail", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EmailFileAssessmentRequest"
