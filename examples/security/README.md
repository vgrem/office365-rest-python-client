# Microsoft 365 Security

Security, threat intelligence, and incident triage via the Microsoft Graph Security API —
attack simulation, IOC enrichment, and alert evidence.

---

## Security & Threat Protection

### [Attack simulation training](attack_simulation.py)

Attack simulation training — list phishing simulation campaigns, automations, payloads, and training assignments.

```python
sim = client.security.attack_simulation

# Phishing simulation campaigns
simulations = sim.simulations.get().execute_query()
for s in simulations:
    print(f"{s.properties.get('displayName')}  status={s.properties.get('status')}  technique={s.properties.get('attackTechnique')}")

# Recurring automations and their runs
for a in sim.simulation_automations.get().execute_query():
    print(f"{a.properties.get('displayName')}  status={a.properties.get('status')}")
    for r in a.runs.get().execute_query():
        print(f"    -> {r.properties.get('status')}  start={r.properties.get('startDateTime')}")

# Landing pages configured for the tenant
print(f"Landing pages: {len(sim.landing_pages.get().execute_query())}")
```


### [Threat intelligence IOC enrichment](threat_intelligence_ioc.py)

Enrich a host (domain or IP) with Microsoft Defender Threat Intelligence.

```python
ti = client.security.threat_intelligence

# Resolve a host and pull its reputation
host = ti.hosts["contoso.com"].get().execute_query()
print(f"First seen: {host.properties.get('firstSeenDateTime')}")

reputation = host.reputation.get().execute_query()
print(f"Reputation: {reputation.properties.get('score')}  ({reputation.properties.get('classification')})")

# Active threat-actor intel profiles
profiles = ti.intel_profiles.get().execute_query()
for profile in profiles:
    print(f"{profile.title}  severity={profile.properties.get('severity')}")
```


### [Incident attack-story summary](incident_attack_story.py)

Summarize the attack story of security incidents from alert evidence.

```python
incidents = client.security.incidents.get().execute_query()

for incident in incidents:
    alerts = incident.alerts.get().execute_query()
    evidence_types = Counter()
    for alert in alerts:
        for evidence in alert.evidence:
            label = (evidence.entity_type_name or "Evidence").split(".")[-1].replace("Evidence", "")
            evidence_types[label] += 1
    print(f"{incident.properties.get('title')}: {len(alerts)} alerts  {dict(evidence_types)}")
```


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
