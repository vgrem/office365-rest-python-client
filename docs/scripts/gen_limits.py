"""Generate the service-limits reference page (mkdocs-gen-files plugin).

The table mirrors :meth:`office365.sharepoint.thresholds.Limits.catalog`, so the
docs can't drift from the code, and adds a **Bound at** column scanned from the
``@limit`` decorators on the model. mkdocs-gen-files executes this module with
``runpy``, so emission happens at module level.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import mkdocs_gen_files  # noqa: E402
from _limit_bindings import scan_bindings  # noqa: E402
from office365.sharepoint.thresholds import Limit, Limits  # noqa: E402

_REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]

_HEADER = """# Service limits

SharePoint enforces the limits below. The library declares them in
`office365.sharepoint.thresholds.Limits` and binds them to the model with the
`@limit` decorator — **warnings by default**, never a silent truncation. The list
view threshold is the one most callers meet; see
[Large lists and folders](large-lists.md) for the paging and indexing recipes.

Sources:

- [SharePoint in Microsoft 365 limits](https://learn.microsoft.com/en-us/office365/servicedescriptions/sharepoint-online-service-description/sharepoint-online-limits)
- [Software boundaries and limits (SharePoint Server 2016/2019)](https://learn.microsoft.com/en-us/sharepoint/install/software-boundaries-limits-2019)

```python
from office365.sharepoint.thresholds import Limits, limit, warn_if_exceeds

warn_if_exceeds(Limits.LIST_VIEW, item_count, context="list 'Orders'")

@limit(Limits.LIST_VIEW, arg="page_size")   # declare + enforce on the model
def get_items(page_size=None): ...
```
"""

_ASSESSMENT = """## Migration assessment

The pre-migration assessment (`MigrationAssessor` / `MigrationTenantAssessor`)
reports several of these limits as [SPMT scan-assessment risk codes](https://learn.microsoft.com/en-us/sharepointmigration/spmt-scan-risk-codes):

| SPMT risk code | Limit | Scanner |
| --- | --- | --- |
| `LIST_VIEW_EXCEED_LIMIT` | list view threshold | `LargeListScanner` |
| `ITEM_COUNT_EXCEED_INDEX_LIMIT` | index add/remove threshold | `LargeListScanner` |
| `ITEM_COUNT_EXCEED_LIMIT` | max items per list/library | `LargeListScanner` |
| `LIST_VIEW_LOOKUP_EXCEED_LIMIT` | list view lookup threshold | `LookupColumnScanner` |
| `UNIQUE_PERMISSION_EXCEED_LIMIT` | unique security scopes | `PermissionScanner` |

Each `AssessmentIssue` carries the `risk_code`, and `report.by_risk_code` groups
the issues by code.
"""


def _emit(path: str, content: str) -> None:
    with mkdocs_gen_files.open(path, "w") as f:
        f.write(content)


_bindings = scan_bindings(_REPO_ROOT / "office365")
_bound: dict[int, list[str]] = {}
for _attr, _obj in vars(Limits).items():
    if isinstance(_obj, Limit) and _bindings.get(_attr):
        _bound.setdefault(id(_obj), []).extend(_bindings[_attr])


def _bound_at(limit: Limit) -> str:
    return ", ".join(sorted(set(_bound.get(id(limit), [])))) or "—"


_rows = [
    "| Limit | Value | Kind | Scope | Bound at | Notes |",
    "| --- | --- | --- | --- | --- | --- |",
]
for _limit in Limits.catalog():
    _name = f"[{_limit.name}]({_limit.doc})" if _limit.doc else _limit.name
    _rows.append(f"| {_name} | {_limit} | {_limit.kind.value} | {_limit.scope} | {_bound_at(_limit)} | {_limit.note} |")

_emit("limits.md", "\n".join([_HEADER, *_rows, "", _ASSESSMENT]))
