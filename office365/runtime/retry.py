"""Generic retry with exponential backoff + jitter — reusable, first-class retry helper.

Follows the Microsoft Graph / SharePoint guidance: honor the server's
``Retry-After`` header when present, otherwise back off exponentially with
jitter (so a fleet of clients doesn't retry in lock-step).
"""

from __future__ import annotations

import random
from functools import wraps
from time import sleep
from typing import Any, Callable, Optional, Tuple, Type

from typing_extensions import ParamSpec

from office365.runtime.client_request_exception import ClientRequestException

_P = ParamSpec("_P")

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
    when it is unavailable or malformed so callers fall back to the backoff.

    Args:
        ex: The exception that was raised
    """
    response = getattr(ex, "response", None)
    if response is None or getattr(response, "status_code", None) not in {429, 503}:
        return None
    return response_retry_after(response)


def response_retry_after(response: Any) -> Optional[int]:
    """Parse the ``Retry-After`` header (seconds) from a response, if any.

    Returns ``None`` when the header is absent or malformed.

    Args:
        response: A ``requests.Response`` (or object exposing ``.headers``)
    """
    if response is None:
        return None
    value = response.headers.get("Retry-After", None)
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def backoff_delay(attempt: int, base: int, max_delay: Optional[int] = None, jitter: bool = True) -> float:
    """Compute the delay before retry ``attempt``.

    Exponential: ``base * 2 ** (attempt - 1)``, capped at ``max_delay``. With
    ``jitter`` enabled (default) the delay is randomized in ``[0, delay]`` per
    the "full jitter" strategy, avoiding synchronized retry storms.

    Args:
        attempt: 1-based retry attempt number.
        base: Base delay in seconds (``timeout_secs``).
        max_delay: Optional upper bound in seconds for the exponential growth.
        jitter: Whether to randomize the delay (default True).

    Returns:
        Seconds to sleep before this attempt.
    """
    delay = base * (2 ** (attempt - 1))
    if max_delay is not None:
        delay = min(delay, max_delay)
    if jitter:
        delay = random.uniform(0, delay)
    return delay


def _run_with_retry(
    func: Callable[[], Any],
    *,
    max_retry: int,
    timeout_secs: int,
    max_delay: Optional[int],
    jitter: bool,
    exceptions: Tuple[Type[Exception], ...],
    is_retriable: Callable[[Exception], bool],
    on_failure: Optional[Callable[[int, Exception], Optional[int]]],
    on_success: Optional[Callable[[Any], None]],
) -> Any:
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
            delay = retry_after if retry_after is not None else backoff_delay(attempt, timeout_secs, max_delay, jitter)
            sleep(delay)
    assert last_ex is not None
    raise last_ex


def retry(
    func: Optional[Callable[[], Any]] = None,
    max_retry: int = 5,
    timeout_secs: int = 5,
    max_delay: Optional[int] = None,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (ClientRequestException,),
    is_retriable: Callable[[Exception], bool] = is_transient_error,
    on_failure: Optional[Callable[[int, Exception], Optional[int]]] = None,
    on_success: Optional[Callable[[Any], None]] = None,
) -> Any:
    """Run ``func`` with retries — or, called without ``func``, return a decorator.

    Permanent failures re-raise immediately; the last exception is re-raised
    once retries are exhausted. The delay between attempts is exponential with
    jitter (:func:`backoff_delay`); when ``on_failure`` returns a delay (e.g.
    the server's ``Retry-After`` via :func:`retry_after_delay`) that value
    overrides the backoff.

    Two forms::

        retry(do_request, max_retry=3)  # run now (existing behaviour)


        @retry(max_retry=3)  # decorate a callable
        def do_request(): ...

    Args:
        func: Callable to execute. Omit to get a decorator.
        max_retry: Maximum number of retry attempts
        timeout_secs: Base delay for exponential backoff (seconds)
        max_delay: Optional cap for the exponential delay (seconds)
        jitter: Whether to randomize the delay (default True)
        exceptions: Exception types that are candidates for retry
        is_retriable: Classifier deciding whether a caught exception is retried
        on_failure: Called after each failed attempt with ``(attempt, ex)``;
            may return a retry delay (seconds) to override the backoff
        on_success: Called with ``func()`` result on success
    """
    options = {
        "max_retry": max_retry,
        "timeout_secs": timeout_secs,
        "max_delay": max_delay,
        "jitter": jitter,
        "exceptions": exceptions,
        "is_retriable": is_retriable,
        "on_failure": on_failure,
        "on_success": on_success,
    }
    if func is None:

        def decorator(fn: Callable[_P, Any]) -> Callable[_P, Any]:
            @wraps(fn)
            def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> Any:
                return _run_with_retry(lambda: fn(*args, **kwargs), **options)  # type: ignore[arg-type]

            return wrapper

        return decorator
    return _run_with_retry(func, **options)  # type: ignore[arg-type]
