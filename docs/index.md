---
title: Home
---

<div class="hero" markdown="1">

# Office 365 REST Python Client

A Python client for the **Microsoft 365 and SharePoint REST APIs** — typed
models, fluent queries, and **hundreds of ready-to-run examples** for Teams,
To-Do, Bookings, Entra ID, OneDrive, and SharePoint.

<div class="hero-actions" markdown="1">

[:fontawesome-solid-rocket: Browse the examples](sharepoint/index.md){ .md-button .md-button--primary }
[:material-book-open-page-variant: Library guide](api.md){ .md-button }

</div>

</div>

## Which client do I need?

| | `ClientContext` | `GraphClient` |
|---|---|---|
| **Target API** | SharePoint REST API v1 | Microsoft Graph API |
| **Use for** | SharePoint lists, files, folders, search, site admin, permissions | Outlook, OneDrive, Teams, OneNote, Planner, Users, Groups |
| **SharePoint via Graph?** | — | Partial — use `ClientContext` for full SharePoint fidelity |
| **Typical auth** | `with_client_certificate`, `with_username_and_password`, device / interactive | `with_client_secret`, `with_certificate`, device / interactive |

## Both clients

### Microsoft Graph — `GraphClient`

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="contoso.onmicrosoft.com").with_client_secret(
    "client_id", "client_secret"
)
me = client.me.get().execute_query()
print(me.user_principal_name)
```

### SharePoint — `ClientContext`

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_certificate(
    tenant="contoso.onmicrosoft.com",
    client_id="client_id",
    thumbprint="thumbprint",
    cert_path="./cert.pem",
)
web = ctx.web.get().execute_query()
print(f"Site title: {web.title}")
```

## Learn more

-   **[Examples](sharepoint/index.md)** — start with the SharePoint area, then
    browse Teams, To-Do, Entra ID, and the rest from the left navigation.
-   **[Library guide](api.md)** — auth flows, query patterns, and power features.
-   **[README](https://github.com/vgrem/office365-rest-python-client#readme)** —
    installation, the full auth matrix, and per-service guides (lists, files,
    Outlook, OneDrive, Teams, …).

New to Microsoft 365 APIs? Start with the [Microsoft Graph docs](https://learn.microsoft.com/en-us/graph/)
or the [SharePoint REST API reference](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api).
