# Microsoft 365 Defender

Examples for working with Microsoft 365 Defender via the Graph Security
API — advanced hunting, incidents, alerts, and secure score.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| `ThreatHunting.Read.All` | Run advanced hunting KQL queries | [Threat hunting permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#threat-hunting-permissions) |
| `Incidents.Read.All` | List and read incidents | [Incident permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#incident-permissions) |
| `Incidents.ReadWrite.All` | Update incidents | [Incident permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#incident-permissions) |
| `SecurityAlert.Read.All` | List and read alerts (v2) | [Security permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#security-permissions) |
| `SecurityEvents.Read.All` | Read Secure Score control profiles | [Security permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#security-permissions) |

Admin consent is required for all permissions above.

---

## Examples

| Scenario | File | Permission |
|---|---|---|
| List incidents | [`list_incidents.py`](./list_incidents.py) | `Incidents.Read.All` |
| Get incident with alerts | [`get_incident_details.py`](./get_incident_details.py) | `Incidents.Read.All` |
| Update incident status | [`update_incident.py`](./update_incident.py) | `Incidents.ReadWrite.All` |
| List security alerts (v2) | [`list_alerts.py`](./list_alerts.py) | `SecurityAlert.Read.All` |
| Run advanced hunting query | [`run_hunting_query.py`](./run_hunting_query.py) | `ThreatHunting.Read.All` |
| Get Secure Score profiles | [`get_secure_score.py`](./get_secure_score.py) | `SecurityEvents.Read.All` |

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
