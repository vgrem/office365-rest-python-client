# Microsoft Purview — Compliance & Information Protection

Examples for working with Microsoft Purview compliance, records
management, sensitivity labels, eDiscovery, subject rights, and
threat assessment.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `RecordsManagement.ReadWrite.All` | Create and manage retention labels | [Records management permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#records-management-permissions) |
| `InformationProtectionPolicy.Read.All` | Read sensitivity labels | |
| `ThreatAssessment.ReadWrite.All` | Submit URL/file threat assessments | |
| `eDiscovery.ReadWrite.All` | Create eDiscovery cases and searches | |
| `SubjectRightsRequest.ReadWrite.All` | Create and manage subject rights requests | |
| `Sites.ReadWrite.All` | Apply labels to SharePoint files | |

---

## Examples

### Records Management

| Scenario | File | Permission |
|---|---|---|
| Create a retention label | [`records/retention_label.py`](./records/retention_label.py) | `RecordsManagement.ReadWrite.All` |
| List retention labels | [`records/list_retention_labels.py`](./records/list_retention_labels.py) | `RecordsManagement.Read.All` |
| Auto-apply label to unlabeled files (Graph) | [`records/auto_apply_retention_label.py`](./records/auto_apply_retention_label.py) | `RecordsManagement.ReadWrite.All` + `Sites.ReadWrite.All` |
| Auto-apply label via SharePoint CSOM | [`records/auto_apply_label.py`](./records/auto_apply_label.py) | `RecordsManagement.ReadWrite.All` + `Sites.Read.All` |

### Sensitivity Labels

| Scenario | File | Permission |
|---|---|---|
| List sensitivity labels | [`sensitivity_labels/apply.py`](./sensitivity_labels/apply.py) | `InformationProtectionPolicy.Read.All` |
| Analyze label usage | [`sensitivity_labels/analytics.py`](./sensitivity_labels/analytics.py) | `InformationProtectionPolicy.Read.All` |

### eDiscovery & Compliance

| Scenario | File | Permission |
|---|---|---|
| eDiscovery full case workflow | [`ediscovery/create_and_search.py`](./ediscovery/create_and_search.py) | `eDiscovery.ReadWrite.All` |
| Search partially indexed items | [`compliance/search_partially_indexed.py`](./compliance/search_partially_indexed.py) | `eDiscovery.ReadWrite.All` |

### Subject Rights

| Scenario | File | Permission |
|---|---|---|
| Create a subject rights request | [`subject_rights/create_request.py`](./subject_rights/create_request.py) | `SubjectRightsRequest.ReadWrite.All` |
| List subject rights requests | [`subject_rights/list_requests.py`](./subject_rights/list_requests.py) | `SubjectRightsRequest.Read.All` |

### Threat Assessment

| Scenario | File | Permission |
|---|---|---|
| Submit URL/file threat assessment | [`threat_assessment/scan_url.py`](./threat_assessment/scan_url.py) | `ThreatAssessment.ReadWrite.All` |

---

## Quick start

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="contoso.onmicrosoft.com").with_client_secret(
    "client_id", "client_secret"
)

labels = client.security.labels.retention_labels.get().execute_query()
for label in labels:
    print(label.display_name)
```

---

## Official docs

- [Microsoft Purview overview](https://learn.microsoft.com/en-us/purview)
- [Records management API](https://learn.microsoft.com/en-us/graph/api/resources/security-recordsmanagement-overview)
- [eDiscovery API](https://learn.microsoft.com/en-us/graph/api/resources/security-ediscoveryoverview)
- [Subject rights request API](https://learn.microsoft.com/en-us/graph/api/resources/security-subjectrightsrequest)
- [Threat assessment API](https://learn.microsoft.com/en-us/graph/api/resources/threatassessment-api-overview)
