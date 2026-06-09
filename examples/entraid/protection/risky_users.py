"""
Risky users and risk detections — Identity Protection reporting and
remediation.

Lists users flagged by Azure AD Identity Protection, reviews their
risk history, shows raw risk detections with IP/location details,
and demonstrates dismiss / confirm-compromise actions.

Security teams use this daily for incident response.

Requires delegated permission ``IdentityRiskyUser.Read.All``,
``IdentityRiskDetection.Read.All`` to read, and
``IdentityRiskyUser.ReadWrite.All`` to dismiss / confirm.

https://learn.microsoft.com/en-us/graph/api/resources/identityprotection-root
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    risky_users = client.identity_protection.risky_users.get().execute_query()
    print(f"Risky users: {len(risky_users)}\n")

    for u in risky_users:
        print(
            f"  {u.user_principal_name}  level={u.risk_level.name}  "
            f"state={u.risk_state.name}  last={u.risk_last_updated_date_time}"
        )
        print(f"    display={u.user_display_name}  deleted={u.is_deleted}  processing={u.is_processing}")

    if risky_users:
        print()
        user = risky_users[0]
        history = user.history.get().execute_query()
        print(f"Risk history for {user.user_principal_name} ({len(history)} events):")
        for h in history:
            dt = h.properties.get("activityDateTime", h.properties.get("detectedDateTime", ""))
            print(f"  {dt}  detail={h.risk_detail}  type={h.properties.get('riskEventType', '?')}")

    since = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    detections = (
        client.identity_protection.risk_detections.filter(f"detectedDateTime ge {since}").top(20).get().execute_query()
    )
    print(f"\nRisk detections (last 7 days): {len(detections)}")

    for d in detections:
        print(
            f"  {d.detected_date_time}  user={d.user_principal_name}  "
            f"risk={d.risk_level.name}  activity={d.activity.name}  ip={d.ip_address}"
        )


if __name__ == "__main__":
    main()
