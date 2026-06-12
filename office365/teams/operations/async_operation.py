from __future__ import annotations

import time
from collections.abc import Callable
from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.runtime.types.odata_property import odata
from office365.teams.operations.async_status import TeamsAsyncOperationStatus
from office365.teams.operations.error import OperationError
from office365.teams.operations.type import TeamsAsyncOperationType


class TeamsAsyncOperation(Entity):
    """
    A Microsoft Teams async operation is an operation that transcends the lifetime of a single API request.
    These operations are long-running or too expensive to complete within the timeframe of their originating request.

    When an async operation is initiated, the method returns a 202 Accepted response code.
    The response will also contain a Location header, which contains the location of the teamsAsyncOperation.
    Periodically check the status of the operation by making a GET request to this location; wait >30 seconds
    between checks. When the request completes successfully, the status will be "succeeded" and
    the targetResourceLocation will point to the created/modified resource.

    """

    def poll_for_status(
        self,
        status_type: TeamsAsyncOperationStatus = TeamsAsyncOperationStatus.succeeded,
        timeout_sec: int = 180,
        polling_interval: int = 15,
        success_callback: Callable[[TeamsAsyncOperation], None] | None = None,
        failure_callback: Callable[[TeamsAsyncOperation], None] | None = None,
    ) -> Self:
        """Poll to check for completion of an async Teams operation.

        Args:
            status_type: The status to wait for (default succeeded)
            timeout_sec: Maximum seconds to wait (default 180)
            polling_interval: Seconds between polls (default 15)
            success_callback: Called on success with the populated operation
            failure_callback: Called on timeout or failed status
        """
        deadline = time.time() + timeout_sec

        def _poll():
            self.get().after_execute(_verify_status, execute_first=True)

        def _verify_status(return_type: TeamsAsyncOperation):
            if return_type.status == status_type:
                if callable(success_callback):
                    success_callback(return_type)
                return
            if return_type.status == TeamsAsyncOperationStatus.failed:
                if callable(failure_callback):
                    failure_callback(return_type)
                return
            if time.time() >= deadline:
                if callable(failure_callback):
                    failure_callback(self)
                return
            time.sleep(polling_interval)
            _poll()

        _poll()
        return self

    @odata(name="attemptsCount")
    @property
    def attempts_count(self) -> Optional[int]:
        """Number of times the operation was attempted before being marked as succeeded or failed."""
        return self.properties.get("attemptsCount", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> datetime:
        """Date and time when the operation was created."""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def error(self) -> OperationError:
        """Error information if the operation failed."""
        return self.properties.get("error", OperationError())

    @odata(name="lastActionDateTime")
    @property
    def last_action_date_time(self) -> datetime:
        """Date and time when the operation was last updated."""
        return self.properties.get("lastActionDateTime", datetime.min)

    @odata(name="operationType")
    @property
    def operation_type(self) -> TeamsAsyncOperationType:
        """The type of the operation."""
        return self.properties.get("operationType", TeamsAsyncOperationType.unknown)

    @property
    def status(self) -> TeamsAsyncOperationStatus:
        """Operation status."""
        return self.properties.get("status", TeamsAsyncOperationStatus.invalid)

    @property
    def target_resource_id(self) -> Optional[str]:
        """The ID of the object that's created or modified as result of this async operation, typically a team."""
        return self.properties.get("targetResourceId", None)

    @property
    def target_resource_location(self) -> Optional[str]:
        """The location of the object that's created or modified as result of this async operation.
        This URL should be treated as an opaque value and not parsed into its component paths.
        """
        return self.properties.get("targetResourceLocation", None)
