"""Generate the throttling guide + limits table (mkdocs-gen-files plugin).

The table mirrors :meth:`office365.graph_limits.GraphLimits.catalog`, so the docs
can't drift from the code, and adds a **Bound at** column scanned from the
``@limit`` decorators. mkdocs-gen-files executes this module with ``runpy``, so
emission happens at module level.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import mkdocs_gen_files  # noqa: E402
from _limit_bindings import scan_bindings  # noqa: E402
from office365.graph_limits import GraphLimits  # noqa: E402
from office365.runtime.limits import Limit  # noqa: E402

_REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]

_HEADER = """# Throttling

Microsoft Graph and SharePoint both throttle with **HTTP 429** and a
`Retry-After` header; Graph also reports how close an app is to its limit. The
library reads these signals, retries with the server's delay (falling back to
exponential backoff with jitter) and can pace a whole fleet proactively.

Unlike SharePoint's static [service limits](limits.md), Graph throttling is
**dynamic** — evaluated per scope (per app, per tenant, per app + tenant, per
resource) and per request type — so the library reacts to the signals rather
than enforcing a fixed budget. The quotas below are reference-only; the model
declares them with `@limit(GraphLimits.X)` (see the **Bound at** column).

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

## Service limits (reference)

The numbers below are the tested limits Graph enforces; the first one reached
triggers throttling. They're reference-only — see
`office365.graph_limits.GraphLimits`.

"""


def _emit(path: str, content: str) -> None:
    with mkdocs_gen_files.open(path, "w") as f:
        f.write(content)


_bindings = scan_bindings(_REPO_ROOT / "office365")
_bound: dict[int, list[str]] = {}
for _attr, _obj in vars(GraphLimits).items():
    if isinstance(_obj, Limit) and _bindings.get(_attr):
        _bound.setdefault(id(_obj), []).extend(_bindings[_attr])


def _bound_at(limit: Limit) -> str:
    return ", ".join(sorted(set(_bound.get(id(limit), [])))) or "—"


_rows = [
    "| Service | Limit | Scope | Type | Bound at | Notes |",
    "| --- | --- | --- | --- | --- | --- |",
]
for _limit in sorted(GraphLimits.catalog(), key=lambda item: (item.name, -item.value)):
    _rows.append(
        f"| {_limit.name} | {_limit} | {_limit.scope} | {_limit.request_type or 'any'} "
        f"| {_bound_at(_limit)} | {_limit.note} |"
    )

_emit("throttling.md", "\n".join([_HEADER, *_rows, ""]))
