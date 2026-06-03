# Examples

Practical examples demonstrating how to use the `office365-rest-python-client`
library across Microsoft 365 and Entra ID services.

---

## Overview

| Directory | Product / API | Covers |
|---|---|---|
| [`auth/`](./auth/) | Graph authentication | Client secret, certificate, interactive, device code, ROPC, GCC High |
| [`defender/`](./defender/) | **Microsoft 365 Defender** | Advanced hunting, incidents, alerts, secure score |
| [`entra-id/`](./entra-id/) | **Microsoft Entra ID** | Users, groups, applications, roles, policies, identity providers |
| [`insights/`](./insights/) | Graph Insights API | Shared documents, trending content |
| [`onedrive/`](./onedrive/) | **Microsoft OneDrive** | Files, folders, drives, sharing, search, versions, thumbnails |
| [`onenote/`](./onenote/) | **Microsoft OneNote** | Notebooks, sections, section groups, pages, content |
| [`outlook/`](./outlook/) | **Outlook / Exchange Online** | Mail (send, draft, folders, rules, search), events, calendars |
| [`planner/`](./planner/) | **Microsoft Planner** | Plans, buckets, tasks, assignments, details |
| [`purview/`](./purview/) | **Microsoft Purview** | eDiscovery cases, retention labels, subject rights requests |
| [`reports/`](./reports/) | M365 usage reports | Email, mailbox, OneDrive, SharePoint, Teams, M365 app, Office activations |
| [`sharepoint/`](./sharepoint/) | **Microsoft SharePoint** | All areas — files, lists, permissions, search, taxonomy, sites, webhooks |
| [`teams/`](./teams/) | **Microsoft Teams** | Lifecycle, channels, messages, members, apps, tabs, settings |

---

## Quick start

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="contoso.onmicrosoft.com").with_client_secret(
    "client_id", "client_secret"
)

web = client.sites.root.web.get().execute_query()
print(f"Connected to: {web.title}")
```

See [`auth/`](./auth/) for all supported authentication flows.

---

## Related

- [Microsoft Graph API documentation](https://learn.microsoft.com/en-us/graph/api/overview)
- [Office 365 REST Python Client on GitHub](https://github.com/vgrem/office365-rest-python-client)
