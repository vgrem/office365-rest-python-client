from __future__ import annotations

import time
from collections.abc import Callable
from datetime import datetime

from typing_extensions import Self

from office365.entity import Entity
from office365.runtime.types.odata_property import odata
from office365.teams.operations.async_status import TeamsAsyncOperationStatus
from office365.teams.operations.error import OperationError
from office365.teams.operations.type import TeamsAsyncOperationType

_NOT_FOUND_STATUS = 404


def wait_for_operation(
    operation: "TeamsAsyncOperation",
    *,
    success_callback: Callable[["TeamsAsyncOperation"], None] | None = None,
    timeout_sec: int = 180,
    interval: int = 15,
) -> None:
    """Schedule polling of an async operation until ``succeeded`` (deferred).

    Queues the operation status GETs via ``after_execute``; the caller's
    ``execute_query()`` drives them. Raises when the operation fails or times
    out.

    Args:
        operation: The async operation to poll.
        success_callback: Called with the populated operation once succeeded.
        timeout_sec: Maximum seconds to wait.
        interval: Seconds between status polls.
    """

    def _on_failed(op) -> None:
        raise RuntimeError(f"Async operation failed: {op.status}")

    operation.poll_for_status(
        TeamsAsyncOperationStatus.succeeded,
        timeout_sec=timeout_sec,
        polling_interval=interval,
        success_callback=success_callback,
        failure_callback=_on_failed,
    )


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

        def _not_found(exc: Exception) -> bool:
            # The operation's location can be briefly unavailable right after the
            # 202 (e.g. "No workflow found with supplied ID") — treat it as a
            # polling gap, not a permanent failure.
            return getattr(getattr(exc, "response", None), "status_code", None) == _NOT_FOUND_STATUS

        def _fail() -> None:
            if callable(failure_callback):
                failure_callback(self)

        def _poll() -> None:
            qry = self.get()

            def _on_error(exc: Exception) -> None:
                if _not_found(exc) and time.time() < deadline:
                    time.sleep(polling_interval)
                    _poll()
                else:
                    _fail()

            qry.after_execute(_verify_status, execute_first=True).on_error(_on_error)

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
                _fail()
                return
            time.sleep(polling_interval)
            _poll()

        _poll()
        return self

    @odata(name="attemptsCount")
    @property
    def attempts_count(self) -> int | None:
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
    def target_resource_id(self) -> str | None:
        """The ID of the object that's created or modified as result of this async operation, typically a team."""
        return self.properties.get("targetResourceId", None)

    @property
    def target_resource_location(self) -> str | None:
        """The location of the object that's created or modified as result of this async operation.
        This URL should be treated as an opaque value and not parsed into its component paths.
        """
        return self.properties.get("targetResourceLocation", None)
