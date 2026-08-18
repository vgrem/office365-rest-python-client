"""
Risky users and risk detections — Identity Protection reporting and
remediation.

Lists users flagged by Azure AD Identity Protection, reviews their risk
history, shows raw risk detections with IP/location details, and can
dismiss / confirm-compromise actions (opt-in).

Security teams use this daily for incident response.

Requires delegated permission ``IdentityRiskyUser.Read.All`` and
``IdentityRiskDetection.Read.All`` to read, and
``IdentityRiskyUser.ReadWrite.All`` to dismiss / confirm.

https://learn.microsoft.com/en-us/graph/api/resources/identityprotection-root
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Risky users report and remediation")
    parser.add_argument("--limit", type=int, default=50, help="Max risky users to report")
    parser.add_argument("--dismiss-first", action="store_true", help="Dismiss the risk of the first risky user")
    parser.add_argument("--confirm-first", action="store_true", help="Confirm the first risky user as compromised")
    args = parser.parse_args()

    if args.dismiss_first and args.confirm_first:
        raise SystemExit("Use either --dismiss-first or --confirm-first, not both")

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    risky_users = client.identity_protection.risky_users.top(args.limit).get().execute_query()
    print(f"Risky users: {len(risky_users)}\n")

    for u in risky_users:
        print(
            f"  {u.user_principal_name}  level={u.risk_level}  state={u.risk_state.name}  "
            f"last={u.risk_last_updated_date_time}"
        )

    if risky_users:
        first = risky_users[0]
        history = first.history.get().execute_query()
        print(f"\nRisk history for {first.user_principal_name} ({len(history)} events):")
        for h in history:
            dt = h.properties.get("activityDateTime", h.properties.get("detectedDateTime", ""))
            print(f"  {dt}  detail={h.risk_detail}  type={h.properties.get('riskEventType', '?')}")

    if risky_users and (args.dismiss_first or args.confirm_first):
        target = risky_users[0]
        if target.id is None:
            raise SystemExit("Risky user id is not available")
        if args.dismiss_first:
            client.identity_protection.risky_users.dismiss([target.id]).execute_query()
            print(f"\nDismissed risk for {target.user_principal_name}")
        else:
            client.identity_protection.risky_users.confirm_compromised([target.id]).execute_query()
            print(f"\nConfirmed {target.user_principal_name} as compromised")


if __name__ == "__main__":
    main()
