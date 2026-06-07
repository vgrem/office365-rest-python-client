from typing import Optional

from office365.directory.protection.threatassessment.requests.request import (
    ThreatAssessmentRequest,
)
from office365.runtime.types.odata_property import odata


class FileAssessmentRequest(ThreatAssessmentRequest):
    """Used to create and retrieve a file threat assessment, derived from threatAssessmentRequest.

    The file can be a text file or Word document or binary file received in an email attachment.
    """

    @odata(name="fileName")
    @property
    def file_name(self) -> Optional[str]:
        """The name of the file to assess."""
        return self.properties.get("fileName", None)
