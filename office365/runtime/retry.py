"""Generic retry with backoff — reusable, first-class retry helper."""

from __future__ import annotations

from time import sleep
from typing import Any, Callable, Optional, Tuple, Type

from office365.runtime.client_request_exception import ClientRequestException

TRANSIENT_STATUS_CODES = frozenset({408, 429, 500, 502, 503, 504})


def is_transient_error(ex: Exception) -> bool:
    """Whether an exception reflects a transient failure worth retrying.

    Non-HTTP errors (e.g. connection/timeout) are treated as transient.
    """
    status_code = getattr(getattr(ex, "response", None), "status_code", None)
    if status_code is None:
        return True
    return status_code in TRANSIENT_STATUS_CODES


def retry_after_delay(ex: Exception) -> Optional[int]:
    """Return the server-requested retry delay for throttling errors.

    Reads the ``Retry-After`` header of a 429/503 response; returns ``None``
    when it is unavailable or malformed so callers fall back to the default.

    Args:
        ex: The exception that was raised
    """
    response = getattr(ex, "response", None)
    if response is None or getattr(response, "status_code", None) not in {429, 503}:
        return None
    retry_after = response.headers.get("Retry-After", None)
    if retry_after is None:
        return None
    try:
        return int(retry_after)
    except (TypeError, ValueError):
        return None


def retry(
    func: Callable[[], Any],
    max_retry: int = 5,
    timeout_secs: int = 5,
    exceptions: Tuple[Type[Exception], ...] = (ClientRequestException,),
    is_retriable: Callable[[Exception], bool] = is_transient_error,
    on_failure: Optional[Callable[[int, Exception], Optional[int]]] = None,
    on_success: Optional[Callable[[Any], None]] = None,
) -> Any:
    """Run ``func``, retrying transient failures with backoff.

    Permanent failures re-raise immediately; the last exception is re-raised
    once retries are exhausted.

    Args:
        func: Callable to execute
        max_retry: Maximum number of retry attempts
        timeout_secs: Delay between retries in seconds
        exceptions: Exception types that are candidates for retry
        is_retriable: Classifier deciding whether a caught exception is retried
        on_failure: Called after each failed attempt with ``(attempt, ex)``;
            may return a retry delay (seconds) to override ``timeout_secs``
        on_success: Called with ``func()`` result on success
    """
    last_ex: Exception | None = None
    for attempt in range(1, max_retry + 1):
        try:
            result = func()
            if callable(on_success):
                on_success(result)
            return result
        except exceptions as e:
            if not callable(is_retriable) or not is_retriable(e):
                raise
            last_ex = e
            retry_after: Optional[int] = None
            if callable(on_failure):
                retry_after = on_failure(attempt, e)
            sleep(retry_after if retry_after is not None else timeout_secs)
    assert last_ex is not None
    raise last_ex
