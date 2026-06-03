# Outlook — Mail, Calendar & Events

Examples for working with Outlook mail, calendar, and events via Microsoft Graph.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| `Mail.ReadWrite` (delegated) | Read, send, and manage messages | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#mail-permissions) |
| `Mail.Send` (delegated) | Send mail on behalf of the signed-in user | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#mail-permissions) |
| `Calendars.ReadWrite` (delegated) | Create, read, update, delete events and calendars | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#calendars-permissions) |
| `User.Read` (delegated) | Access the signed-in user's profile and mailbox | Included by default |

Admin consent is required for tenant-wide permissions.

---

## Directories

| Directory | Covers |
|---|---|
| [`messages/`](./messages/) | Send, draft, list, search, move, reply, forward, folders, inbox rules, categories, automatic replies, subscriptions |
| [`events/`](./events/) | Create, list, update, delete, accept, decline, recurring, cancel calendar events |
| [`calendars/`](./calendars/) | List, create, delete calendars, find meeting times, get schedule, share, calendar view |

---

## Quick start

```python
from office365.graph_client import GraphClient

# Option A: Client secret (app-only) — for background services
client = GraphClient(tenant="contoso.onmicrosoft.com").with_client_secret(
    "client_id", "client_secret"
)

# Option B: Interactive browser login — for desktop apps
# client = GraphClient(tenant="contoso.onmicrosoft.com").with_token_interactive(
#     "client_id"
# )

# Fetch the user and send a test message
client.me.send_mail(
    subject="Hello from the library",
    body="This email was sent using MS Graph.",
    to_recipients=["user@contoso.com"],
).execute_query()
```

All examples use `GraphClient` with `with_username_and_password()` (MSAL ROPC) by default.
You can replace with any supported auth flow — see [`examples/auth/`](/examples/auth) for all options.

---

## Official docs

- [Outlook mail API overview](https://learn.microsoft.com/en-us/graph/api/resources/message)
- [Outlook calendar API overview](https://learn.microsoft.com/en-us/graph/api/resources/event)
- [Microsoft Graph permissions reference](https://learn.microsoft.com/en-us/graph/permissions-reference)
