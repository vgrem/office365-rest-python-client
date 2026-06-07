from datetime import datetime
from typing import Optional

from office365.directory.permissions.identity_set import IdentitySet
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class ThreatAssessmentRequest(Entity):
    """An abstract resource type used to represent a threat assessment request item."""

    @odata(name="createdBy")
    @property
    def created_by(self) -> IdentitySet:
        """The threat assessment request creator."""
        return self.properties.get("createdBy", IdentitySet())

    @odata(name="createdDateTime")
    @property
    def created_datetime(self) -> datetime:
        """
        The Timestamp type represents date and time information using ISO 8601 format and is always in UTC time.
        For example, midnight UTC on Jan 1, 2014 is 2014-01-01T00:00:00Z
        """
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def status(self) -> Optional[str]:
        """The threat assessment status. Possible values are: pending, completed."""
        return self.properties.get("status", None)

    @odata(name="expectedAssessment")
    @property
    def expected_assessment(self) -> Optional[str]:
        """The expected assessment from submitter. Possible values: block, unblock."""
        return self.properties.get("expectedAssessment", None)

    @property
    def category(self) -> Optional[str]:
        """The threat category. Possible values: spam, phishing, malware."""
        return self.properties.get("category", None)
