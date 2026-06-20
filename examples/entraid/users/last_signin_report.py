"""
Find users with no recent successful sign-in.

Requires delegated permissions User.Read.All, AuditLog.Read.All.
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
    cutoff = datetime.now(timezone.utc) - timedelta(days=90)

    for u in client.users.select(
        ["id", "displayName", "userPrincipalName", "userType", "signInActivity"]
    ).execute_query():
        act = u.sign_in_activity
        last = act.lastSuccessfulSignInDateTime or act.lastSignInDateTime
        if last is None or last < cutoff:
            print(f"  {u.user_principal_name}  last sign-in: {last}")


if __name__ == "__main__":
    main()
