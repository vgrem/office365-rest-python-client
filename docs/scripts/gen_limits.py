"""Generate the service-limits reference page (mkdocs-gen-files plugin).

The table mirrors :meth:`office365.sharepoint.thresholds.Limits.catalog`, so the
docs can't drift from the code. mkdocs-gen-files executes this module with
``runpy``, so emission happens at module level.
"""

from __future__ import annotations

import mkdocs_gen_files
from office365.sharepoint.thresholds import Limits

_HEADER = """# Service limits

SharePoint enforces the limits below. The library declares them in
`office365.sharepoint.thresholds.Limits` and guard-rails the call sites that can
hit them — **warnings by default**, never a silent truncation. The list view
threshold is the one most callers meet; see
[Large lists and folders](large-lists.md) for the paging and indexing recipes.

Sources:

- [SharePoint in Microsoft 365 limits](https://learn.microsoft.com/en-us/office365/servicedescriptions/sharepoint-online-service-description/sharepoint-online-limits)
- [Software boundaries and limits (SharePoint Server 2016/2019)](https://learn.microsoft.com/en-us/sharepoint/install/software-boundaries-limits-2019)

```python
from office365.sharepoint.thresholds import Limits, warn_if_exceeds

warn_if_exceeds(Limits.LIST_VIEW, item_count, context="list 'Orders'")
```
"""


def _emit(path: str, content: str) -> None:
    with mkdocs_gen_files.open(path, "w") as f:
        f.write(content)


_rows = ["| Limit | Value | Kind | Scope | Notes |", "| --- | --- | --- | --- | --- |"]
for _limit in Limits.catalog():
    _name = f"[{_limit.name}]({_limit.doc})" if _limit.doc else _limit.name
    _rows.append(f"| {_name} | {_limit} | {_limit.kind.value} | {_limit.scope} | {_limit.note} |")

_emit("limits.md", "\n".join([_HEADER, *_rows, ""]))
