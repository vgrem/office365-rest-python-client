# Insights

Documents that matter to a user right now — trending, recently used, and shared
with them — from the Microsoft Graph Insights API.

Insights are a per-user shortcut across OneDrive and SharePoint: Graph ranks the
content and returns a `resourceReference` you can resolve to a drive item.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `Sites.Read.All` (delegated) | Read the signed-in user's insights | [Insights permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#sites-permissions) |

---

## Examples

| Operation | File | API |
|---|---|---|
| Trending, used, and shared documents in one report | [`insights_report.py`](./insights_report.py) | [insights resource](https://learn.microsoft.com/en-us/graph/api/resources/insights) |

---

## Quick start

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="contoso.onmicrosoft.com").with_token_interactive("client_id")

for item in client.me.insights.trending.get().execute_query():
    print(item.resource_reference)
```

---

## API reference

- [Insights resource](https://learn.microsoft.com/en-us/graph/api/resources/insights)
- [Trending](https://learn.microsoft.com/en-us/graph/api/resources/insights-trending) /
  [Used](https://learn.microsoft.com/en-us/graph/api/resources/insights-used) /
  [Shared](https://learn.microsoft.com/en-us/graph/api/resources/insights-shared)
