# Microsoft 365 Defender

Examples for working with Microsoft 365 Defender via the Graph Security
API — advanced hunting, incidents, alerts, and secure score.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| `ThreatHunting.Read.All` | Run advanced hunting KQL queries | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#threat-hunting-permissions) |
| `Incidents.Read.All` | List and read incidents | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#incident-permissions) |
| `SecurityAlert.Read.All` | List and read alerts (v2) | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#security-permissions) |
| `SecurityEvents.Read.All` | Read Secure Score control profiles | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#security-permissions) |

Admin consent is required for all permissions above.

---

## Examples

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **1** | Run an advanced hunting KQL query | [`run_hunting_query.py`](./run_hunting_query.py) | `ThreatHunting.Read.All` | [hunting query](https://learn.microsoft.com/en-us/graph/api/security-security-runhuntingquery) |
| **2** | List incidents | [`list_incidents.py`](./list_incidents.py) | `Incidents.Read.All` | [list incidents](https://learn.microsoft.com/en-us/graph/api/security-list-incidents) |
| **3** | List security alerts (v2) | [`list_alerts.py`](./list_alerts.py) | `SecurityAlert.Read.All` | [list alerts](https://learn.microsoft.com/en-us/graph/api/security-list-alerts_v2) |
| **4** | Get Secure Score control profiles | [`get_secure_score.py`](./get_secure_score.py) | `SecurityEvents.Read.All` | [secure score](https://learn.microsoft.com/en-us/graph/api/security-list-securescorecontrolprofiles) |

---

## Quick start

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="contoso.onmicrosoft.com").with_client_secret(
    "client_id", "client_secret"
)

incidents = client.security.incidents.get().execute_query()
for inc in incidents:
    print(f"[{inc.severity}] {inc.display_name}")
```

---

## Official docs

- [Microsoft 365 Defender overview](https://learn.microsoft.com/en-us/microsoft-365/security/defender)
- [Microsoft Graph Security API](https://learn.microsoft.com/en-us/graph/api/resources/security-api-overview)
- [Microsoft Graph Security permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#security-permissions)
