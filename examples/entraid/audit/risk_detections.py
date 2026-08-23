"""
Report identity-protection risk detections.

Risk detections (unfamiliar sign-in properties, anonymous IPs, leaked
credentials, ...) flag accounts that may be compromised. Useful for triaging
Identity Protection signals.

Requires delegated permission ``IdentityRiskEvent.Read.All``.

https://learn.microsoft.com/en-us/graph/api/riskdetection-list
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Report identity-protection risk detections")
    parser.add_argument("--top", type=int, default=50, help="number of detections to show (default 50)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    detections = client.identity_protection.risk_detections.top(args.top).get().execute_query()

    print(f"Risk detections ({len(detections)}):")
    for d in detections:
        print(
            f"  {d.activity_date_time:%Y-%m-%d %H:%M}  {d.user_principal_name or '?':35s}  "
            f"risk={d.risk_level.value:10s}  state={d.risk_state.value:8s}  "
            f"event={d.risk_event_type or '?'}  ip={d.ip_address or '?'}"
        )


if __name__ == "__main__":
    main()
