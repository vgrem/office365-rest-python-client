"""
Summarize the attack story of security incidents from alert evidence.

For each active incident (or a specific one) pulls the linked alerts and their
evidence, aggregates the evidence by type and prints the indicators of
compromise found — a compact view for security operations triage.

Requires delegated permissions ``SecurityIncident.Read.All`` and
``SecurityEvents.Read.All``.

https://learn.microsoft.com/en-us/graph/api/security-list-incidents
https://learn.microsoft.com/en-us/graph/api/security-incident-list-alerts
https://learn.microsoft.com/en-us/graph/api/resources/alertevidence
"""

import argparse
from collections import Counter

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

# Candidate indicator fields per evidence type (keyed by the @odata.type suffix).
EVIDENCE_VALUE_FIELDS = {
    "FileEvidence": ("fileName", "filePath"),
    "IpEvidence": ("ipAddress",),
    "UrlEvidence": ("url",),
    "HostEvidence": ("fqdn",),
    "DeviceEvidence": ("deviceName",),
    "ProcessEvidence": ("processName",),
    "MalwareEvidence": ("malwareName",),
    "RegistryKeyEvidence": ("registryKey", "registryValueName"),
    "MailboxEvidence": ("mailboxAddress", "displayName"),
    "UserEvidence": ("userPrincipalName",),
    "NetworkConnectionEvidence": ("destinationIp", "destinationPort"),
    "CloudApplicationEvidence": ("appId", "instanceId"),
}


def _evidence_label(item) -> str:
    """Short type label for an evidence item, e.g. FileEvidence -> File."""
    name = item.entity_type_name or "AlertEvidence"
    return name.split(".")[-1].replace("Evidence", "")


def _evidence_value(item, label: str) -> str:
    """First non-empty indicator field for an evidence item."""
    for key in EVIDENCE_VALUE_FIELDS.get(label, ()):
        value = item.get_property(key)
        if value:
            return str(value)
    return "?"


def _attack_story(client, incident) -> None:
    """Print a single incident attack story."""
    alerts = incident.alerts.get().execute_query()
    evidence_types = Counter()
    iocs = set()

    for alert in alerts:
        for evidence in alert.evidence:
            label = _evidence_label(evidence)
            evidence_types[label] += 1
            value = _evidence_value(evidence, label)
            if value not in ("?", ""):
                iocs.add(f"{label}: {value}")

    print(f"\nIncident: {incident.properties.get('title', '?')}")
    print(
        f"  Severity: {incident.properties.get('severity', '?')}  "
        f"status: {incident.properties.get('status', '?')}  alerts: {len(alerts)}"
    )
    print(f"  Evidence by type: {dict(evidence_types) or 'none'}")
    if iocs:
        print("  Indicators of compromise:")
        for ioc in sorted(iocs):
            print(f"    - {ioc}")
    else:
        print("  No detailed evidence available.")


def main():
    parser = argparse.ArgumentParser(description="Incident attack-story summary")
    parser.add_argument("--incident-id", default=None, help="optional incident id; defaults to all active incidents")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    if args.incident_id:
        incident = client.security.incidents[args.incident_id].get().execute_query()
        _attack_story(client, incident)
        return

    incidents = client.security.incidents.filter("status eq 'active'").get().execute_query()
    print(f"{len(incidents)} active incident(s)")
    for incident in incidents:
        _attack_story(client, incident)


if __name__ == "__main__":
    main()
