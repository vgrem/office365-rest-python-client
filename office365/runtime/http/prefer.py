"""``Prefer`` request-header helpers.

The ``Prefer`` header opts a single request into non-default server behaviour.
Currently the client exposes the shared-lock bypass used when a file is open
for editing (e.g. in Office) and would otherwise be rejected with HTTP 423.
"""

from __future__ import annotations

from office365.runtime.http.request_options import RequestOptions

#: Value of the ``Prefer`` header that bypasses a *shared lock* on a file.
BYPASS_SHARED_LOCK = "bypass-shared-lock"


def prefer_bypass_shared_lock(request: RequestOptions) -> None:
    """Attach ``Prefer: bypass-shared-lock`` to a request.

    A shared lock (as opposed to a check-out lock) is placed on a file while it
    is open for coauthoring. Only some operations honour the bypass - notably
    delete. Content uploads cannot bypass a shared lock.

    Attach it to a single request with ``context.before_execute``, or pass
    ``bypass_shared_lock=True`` to ``delete_object``.
    """
    request.set_header("Prefer", BYPASS_SHARED_LOCK)
