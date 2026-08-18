"""
Report attack simulation (phishing training) campaigns.

Requires delegated permission ``AttackSimulation.Read.All``.

https://learn.microsoft.com/en-us/graph/api/security-list-attacksimulation
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Attack simulation campaigns report")
    parser.add_argument("--limit", type=int, default=20, help="Max campaigns to show")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    simulations = client.security.attack_simulation.simulations.top(args.limit).get().execute_query()
    print(f"Attack simulation campaigns ({len(simulations)}):\n")
    for s in simulations:
        props = s.properties
        print(f"  {props.get('displayName', '(unnamed)'):40s}  status={props.get('status', '?')}")

    if simulations:
        report = simulations[0].report
        print(f"\nReport for '{simulations[0].properties.get('displayName')}':")
        print(f"  {report.properties}")


if __name__ == "__main__":
    main()
