"""
Risk detections report — filter Identity Protection risk detections by
time window and risk level.

Requires delegated permission ``IdentityRiskDetection.Read.All``.

https://learn.microsoft.com/en-us/graph/api/riskdetection-list
"""

import argparse
from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Risk detections report")
    parser.add_argument("--days", type=int, default=7, help="Look back window in days")
    parser.add_argument("--min-risk", choices=["low", "medium", "high"], default=None, help="Minimum risk level")
    parser.add_argument("--limit", type=int, default=50, help="Max detections")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    since = (datetime.now(timezone.utc) - timedelta(days=args.days)).isoformat()
    detections = client.identity_protection.risk_detections.filter(f"detectedDateTime ge {since}").top(args.limit).get()

    detections = detections.execute_query()
    if args.min_risk:
        order = {"low": 0, "medium": 1, "high": 2}
        detections = [d for d in detections if order.get(d.risk_level.name, 0) >= order[args.min_risk]]

    print(f"Risk detections (last {args.days} days): {len(detections)}\n")
    for d in detections:
        print(
            f"  {d.detected_date_time}  user={d.user_principal_name}  risk={d.risk_level.name}"
            f"  activity={d.activity.name}  ip={d.ip_address}"
        )


if __name__ == "__main__":
    main()
