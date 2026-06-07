# Exchange Online

Examples for working with Exchange Online via Graph API —
mailbox reports, shared mailboxes, and mail flow monitoring.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `User.Read.All` | Read user properties and mailbox settings | [User permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#user-permissions) |
| `Mail.ReadWrite` | Read mailbox settings and forwarding config | [Mail permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#mail-permissions) |

---

## Patterns

| Category | Scenario | File |
|---|---|---|
| **Mailboxes** | Mailbox audit: auto-replies, settings | [`mailboxes/report.py`](./mailboxes/report.py) |
| **Shared mailboxes** | List shared mailboxes, check configuration | [`shared_mailboxes/report.py`](./shared_mailboxes/report.py) |
| **Mail flow** | Detect external forwarding for security audit | [`mail_flow/forwarding_report.py`](./mail_flow/forwarding_report.py) |

---

## Quick start

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="contoso.onmicrosoft.com").with_client_secret(
    "client_id", "client_secret"
)

users = client.users.top(10).get().execute_query()
for u in users:
    print(f"{u.display_name}  ({u.user_principal_name})")
```

---

## Official docs

- [Exchange Online overview](https://learn.microsoft.com/en-us/exchange/exchange-online)
- [Mailbox settings API](https://learn.microsoft.com/en-us/graph/api/resources/mailboxsettings)
- [User mailbox API](https://learn.microsoft.com/en-us/graph/api/resources/user)
