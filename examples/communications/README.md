# Microsoft Teams — Communications

Examples for working with presence, calls, and online meetings
via the Microsoft Graph Communications API.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `Presence.Read` (delegated) | Read a user's presence | [Presence permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#presence-permissions) |
| `Presence.Read.All` (application) | Read presence for all users | |
| `Presence.ReadWrite` (delegated) | Set your own presence and status message | |

---

## Examples

| Scenario | File | Permission |
|---|---|---|
| Get presence for a user | [`get_presence.py`](./get_presence.py) | `Presence.Read` |
| Set presence and status message | [`set_presence.py`](./set_presence.py) | `Presence.ReadWrite` |
| Presence monitor with polling and routing | [`presence/teams_presence_monitor.py`](teams_presence_monitor.py) | `Presence.Read.All`, `Presence.ReadWrite` |

---

## Quick start

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="contoso.onmicrosoft.com").with_username_and_password(
    "client_id", "user@contoso.com", "password"
)

presence = client.me.presence.get().execute_query()
print(f"{presence.availability}  {presence.activity}")
```

---

## Official docs

- [Presence API overview](https://learn.microsoft.com/en-us/graph/api/resources/presence)
- [Cloud communications API](https://learn.microsoft.com/en-us/graph/api/resources/communications-api-overview)
