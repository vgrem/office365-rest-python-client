"""Generate the throttling guide + quotas table (mkdocs-gen-files plugin).

The table is derived from the **model** — the ``@limit`` declarations on the
Graph resource classes — so it can't drift from the code. mkdocs-gen-files
executes this module with ``runpy``, so emission happens at module level.
"""

from __future__ import annotations

import mkdocs_gen_files
from office365.communications.callrecords.call_record import CallRecord
from office365.communications.calls.call import Call
from office365.communications.presences.presence import Presence
from office365.communications.virtualevents.virtual_event import VirtualEvent
from office365.directory.domains.domain import Domain
from office365.directory.licenses.subscribed_sku import SubscribedSku
from office365.directory.objects.object import DirectoryObject
from office365.onedrive.workbooks.workbook import Workbook

#: The Graph resource classes that declare throttling quotas (``@limit``).
_QUOTA_CLASSES = (
    DirectoryObject,
    SubscribedSku,
    Domain,
    CallRecord,
    Workbook,
    Call,
    Presence,
    VirtualEvent,
)

_HEADER = """# Throttling

Microsoft Graph and SharePoint both throttle with **HTTP 429** and a
`Retry-After` header; Graph also reports how close an app is to its limit. The
library reads these signals, retries with the server's delay (falling back to
exponential backoff with jitter) and can pace a whole fleet proactively.

Unlike SharePoint's static [service limits](limits.md), Graph throttling is
**dynamic** — evaluated per scope (per app, per tenant, per app + tenant, per
resource) and per request type — so the library reacts to the signals rather
than enforcing a fixed budget. The quotas below are declared on the Graph
resource classes with `@limit(...)` (reference-only) and shown in the **Bound
at** column.

## Signals

| Header | Direction | Meaning |
| --- | --- | --- |
| `Retry-After` | response | Seconds to wait before retrying a 429/503 |
| `x-ms-throttle-limit-percentage` | response | Share of the limit consumed (`0.8`–`1.8`); `>= 1.0` means throttling |
| `x-ms-resource-unit` | response | The cost of this request (Identity resource units) |
| `x-ms-throttle-scope` | response | The throttled scope (`<Scope>/<Limit>/<AppId>/<TenantId...>`) |
| `x-ms-throttle-information` | response | Why (`CPULimitExceeded`, `WriteLimitExceeded`, ...) |
| `x-ms-throttle-priority` | request | `low` / `normal` / `high` — low is throttled first |

## What the library does

```python
result = client.users.top(10).get().execute_query_retry()   # honor Retry-After + backoff
client.execute_batch(concurrency=5)                         # retries throttled sub-requests

client.with_rate_limit()          # pace a fleet from the signals (proactive)
client.with_throttle_priority("low")     # mark background work low priority
```

`client.with_rate_limit()` reads every response (including batch sub-responses)
and gates the group on `Retry-After`, Graph's `x-ms-throttle-limit-percentage`
and SharePoint's health score. See
`office365.runtime.http.throttling` and `office365.runtime.retry`.

## Best practices to avoid throttling

- Prefer **delta queries** and **change notifications** over polling/scanning.
- **Batch** related operations (JSON batching) and reduce operations per request.
- Don't retry immediately — honor `Retry-After` (the fastest recovery).
- For bulk extraction, use **Microsoft Graph Data Connect** (not throttled).

## Quotas (reference)

The numbers below are the tested limits Graph enforces; the first one reached
triggers throttling. They're declared on the model (`@limit`) — see the
**Bound at** column.

"""


def _emit(path: str, content: str) -> None:
    with mkdocs_gen_files.open(path, "w") as f:
        f.write(content)


# Collect each distinct quota and the classes that declare it (dedup by identity).
_quotas: dict[int, tuple[object, list[str]]] = {}
for _cls in _QUOTA_CLASSES:
    for _limit in _cls.declared_limits():
        _entry = _quotas.setdefault(id(_limit), (_limit, []))
        _entry[1].append(_cls.__name__)

_rows = [
    "| Service | Limit | Scope | Type | Bound at |",
    "| --- | --- | --- | --- | --- |",
]
for _limit, _classes in sorted(_quotas.values(), key=lambda item: (item[0].name, -item[0].value)):  # type: ignore[attr-defined]
    _rows.append(
        f"| {_limit.name} | {_limit} | {_limit.scope} | {_limit.request_type or 'any'} "  # type: ignore[attr-defined]
        f"| {', '.join(_classes)} |"
    )

_emit("throttling.md", "\n".join([_HEADER, *_rows, ""]))
