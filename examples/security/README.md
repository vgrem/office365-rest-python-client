# Microsoft 365 Security

Examples for security, compliance, and threat protection APIs.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `AttackSimulation.Read.All` | Read attack simulation data | [Attack simulation permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#attack-simulation-permissions) |
| `SecurityEvents.Read.All` | Read security events | [Security permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#security-permissions) |

---

## Examples

| Scenario | File | Permission |
|---|---|---|
| Attack simulation training | [`attack_simulation.py`](./attack_simulation.py) | `AttackSimulation.Read.All` |

---

## Related directories

| Directory | What it covers |
|---|---|
| [`examples/defender/`](../defender/) | Incidents, alerts, hunting, secure score |
| [`examples/purview/`](../purview/) | Compliance, eDiscovery, records, labels |
| [`examples/entraid/audit/`](../entraid/audit/) | Directory audit and sign-in logs |

---

## Official docs

- [Microsoft Graph Security API](https://learn.microsoft.com/en-us/graph/api/resources/security-api-overview)
- [Attack simulation and training API](https://learn.microsoft.com/en-us/graph/api/resources/attacksimulationroot)
