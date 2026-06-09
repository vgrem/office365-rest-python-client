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

    idp = client.identity_protection

    # -- Step 1: list risky users with risk level and state --
    risky_users = idp.risky_users.get().execute_query()
    print(f"Risky users: {len(risky_users)}\n")

    for u in risky_users:
        level = u.risk_level.name if u.risk_level else "?"
        state = u.risk_state.name if u.risk_state else "?"
        last = u.risk_last_updated_date_time
        last_str = last.strftime("%Y-%m-%d") if last else "?"
        print(f"  {u.user_principal_name:35s}  level={level:8s}  state={state:12s}  last={last_str}")
        # Details
        print(f"    display={u.user_display_name}  deleted={u.is_deleted}  processing={u.is_processing}")

    # -- Step 2: show recent risk history for the first risky user --
    if risky_users:
        print()
        user = risky_users[0]
        history = user.history.get().execute_query()
        print(f"Risk history for {user.user_principal_name} ({len(history)} events):")
        for h in history:
            dt = h.properties.get("activityDateTime", h.properties.get("detectedDateTime", ""))
            detail = h.properties.get("riskDetail", "?")
            event_type = h.properties.get("riskEventType", "?")
            print(f"  {str(dt)[:19]}  detail={detail:25s}  type={event_type}")

    # -- Step 3: list recent risk detections --
    since = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    detections = idp.risk_detections.filter(f"detectedDateTime ge {since}").top(20).get().execute_query()
    print(f"\nRisk detections (last 7 days): {len(detections)}")

    for d in detections:
        dt = d.detected_date_time.strftime("%m-%d %H:%M") if d.detected_date_time else "?"
        ip = d.ip_address or "?"
        loc = d.location
        city = loc.city if loc and hasattr(loc, "city") and loc.city else ""
        country = loc.country_or_region if loc and hasattr(loc, "country_or_region") and loc.country_or_region else ""
        location_str = f"{city}, {country}" if city or country else ""
        print(
            f"  {dt}  user={d.user_principal_name:30s}  risk={d.risk_level.name:10s}  "
            f"activity={d.activity.name or '?':12s}  "
            f"ip={ip:15s}  {location_str}"
        )

    # -- Step 4: dismiss and confirm-compromise (commented out by default) --

    # Dismiss: marks user risk level as "none" (false positive)
    # idp.risky_users.dismiss(user_ids=["<user-id>"]).execute_query()

    # Confirm compromised: marks as "high" (confirmed breach)
    # idp.risky_users.confirm_compromised(user_ids=["<user-id>"]).execute_query()

    #
    # Example output:
    #   To dismiss a user in the CLI:
    #     client.identity_protection.risky_users.dismiss(
    #         user_ids=["user-id-here"]
    #     ).execute_query()

    # -- Summary --
    print("\n--- Summary ---")
    print(f"Risky users: {len(risky_users)}")
    high_risk = [u for u in risky_users if u.risk_level and u.risk_level.name == "high"]
    print(f"High risk: {len(high_risk)}")
    print(f"Risk detections (7d): {len(detections)}")


if __name__ == "__main__":
    main()
