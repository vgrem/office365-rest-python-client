# Microsoft Purview (Compliance)

Examples for working with Microsoft Purview via the Graph Security API —
eDiscovery cases, retention labels, and subject rights requests.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| `eDiscovery.Read.All` | List and read eDiscovery cases | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#ediscovery-permissions) |
| `RecordsManagement.Read.All` | List and read retention labels | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#records-management-permissions) |
| `SubjectRightsRequest.Read.All` | List subject rights requests | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#subject-rights-request-permissions) |

Admin consent is required for all permissions above.

---

## Examples

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **1** | List eDiscovery cases | [`list_ediscovery_cases.py`](./list_ediscovery_cases.py) | `eDiscovery.Read.All` | [list eDiscovery cases](https://learn.microsoft.com/en-us/graph/api/security-list-ediscoverycases) |
| **2** | List retention labels | [`list_retention_labels.py`](./list_retention_labels.py) | `RecordsManagement.Read.All` | [list retention labels](https://learn.microsoft.com/en-us/graph/api/security-list-retentionlabels) |
| **3** | List subject rights requests | [`list_subject_rights_requests.py`](./list_subject_rights_requests.py) | `SubjectRightsRequest.Read.All` | [list SRR](https://learn.microsoft.com/en-us/graph/api/security-list-subjectrightsrequests) |

---

## Quick start

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="contoso.onmicrosoft.com").with_client_secret(
    "client_id", "client_secret"
)

cases = client.security.cases.ediscovery_cases.get().execute_query()
for case in cases:
    print(f"{case.display_name}  status: {case.status}")
```

---

## Official docs

- [Microsoft Purview overview](https://learn.microsoft.com/en-us/purview)
- [eDiscovery API](https://learn.microsoft.com/en-us/graph/api/resources/security-ediscoverycase)
- [Retention labels API](https://learn.microsoft.com/en-us/graph/api/resources/security-retentionlabel)
- [Subject Rights Request API](https://learn.microsoft.com/en-us/graph/api/resources/security-subjectrightsrequest)
