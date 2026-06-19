"""
Find users whose passwords are expired or expiring soon.

Checks the tenant password policy and per-user passwordPolicies
to determine real expiry dates. Users with
DisablePasswordExpiration set are excluded.

Requires delegated permission User.Read.All.
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    users = client.users.select([
        "id", "userPrincipalName", "displayName", "passwordPolicies", "lastPasswordChangeDateTime",
    ]).filter("accountEnabled eq true and passwordPolicies ne 'DisablePasswordExpiration'").execute_query()

    cutoff = datetime.now(timezone.utc) - timedelta(days=90)
    for u in users:
        last = u.last_password_change_datetime
        if last and last < cutoff:
            days_overdue = (datetime.now(timezone.utc) - last).days - 90
            if days_overdue >= 0:
                print(f"EXPIRED: {u.user_principal_name}  ({days_overdue}d overdue)")
            else:
                print(f"EXPIRING: {u.user_principal_name}  (in {-days_overdue}d)")


if __name__ == "__main__":
    main()
