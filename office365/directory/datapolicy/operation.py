from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.pollable import PollableOperation
from office365.runtime.types.odata_property import odata


class DataPolicyOperation(PollableOperation, Entity):
    """
    Represents a submitted data policy operation. It contains necessary information for tracking the status of
    an operation. For example, a company administrator can submit a data policy operation request to export an
    employee's company data, and then later track that request.
    """

    @odata(name="completedDateTime")
    @property
    def completed_datetime(self) -> datetime:
        """Represents when the request for this data policy operation was completed"""
        return self.properties.get("completedDateTime", datetime.min)

    @odata(name="progress")
    @property
    def progress(self) -> Optional[float]:
        """Specifies the progress of an operation."""
        return self.properties.get("progress", None)

    @odata(name="status")
    @property
    def status(self) -> Optional[str]:
        """Possible values are: notStarted, running, complete, failed, unknownFutureValue."""
        return self.properties.get("status", None)

    @odata(name="storageLocation")
    @property
    def storage_location(self) -> Optional[str]:
        """The URL location to where data is being exported for export requests."""
        return self.properties.get("storageLocation", None)

    @odata(name="submittedDateTime")
    @property
    def submitted_datetime(self) -> datetime:
        """Represents when the request for this data operation was submitted"""
        return self.properties.get("submittedDateTime", datetime.min)

    @odata(name="userId")
    @property
    def user_id(self) -> Optional[str]:
        """The id for the user on whom the operation is performed."""
        return self.properties.get("userId", None)
