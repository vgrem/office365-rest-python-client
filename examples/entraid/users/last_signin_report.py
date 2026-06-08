"""
Report on users with no recent successful sign-in.

Helps identify stale or unused accounts for cleanup. Useful for
license reclamation, security review of dormant accounts, and
Entra ID lifecycle management.

Inspired by ReportLastAccountSignIn-Mg.PS1 and
Find-InactiveLicensedUserAccounts.PS1 from Office 365 for IT Pros.

Required delegated permissions:
    User.Read.All           Read user profiles
    AuditLog.Read.All       Read sign-in logs
    Directory.Read.All      (optional) for detailed sign-in data

https://learn.microsoft.com/en-us/graph/api/resources/signinactivity
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def last_signin_report(days_threshold: int = 90) -> list[dict]:
    """Find users who haven't signed in recently.

    Args:
        days_threshold: Days without a sign-in to flag the account.

    Returns:
        List of user dicts sorted by most recently active first.
    """
    client = GraphClient(tenant=test_tenant).with_client_secret(
        test_client_id, test_client_secret
    )

    # Fetch users with sign-in activity data
    users = client.users.select(["id", "displayName", "userPrincipalName",
                                  "userType", "signInActivity"]).get().execute_query()

    cutoff = datetime.now(timezone.utc) - timedelta(days=days_threshold)
    inactive = []

    for user in users:
        activity = getattr(user, "sign_in_activity", None)
        last = None

        if activity:
            last = getattr(activity, "last_successful_sign_in_date_time", None)
            if not last:
                last = getattr(activity, "last_sign_in_date_time", None)

        if last and last < cutoff:
            days_since = (datetime.now(timezone.utc) - last).days
            inactive.append({
                "upn": user.user_principal_name,
                "display_name": user.display_name,
                "user_type": getattr(user, "user_type", "Member"),
                "last_signin": last,
                "days_since": days_since,
            })
        elif not last:
            # Never signed in
            inactive.append({
                "upn": user.user_principal_name,
                "display_name": user.display_name,
                "user_type": getattr(user, "user_type", "Member"),
                "last_signin": None,
                "days_since": days_threshold + 1,
            })

    inactive.sort(key=lambda x: x["days_since"], reverse=True)
    return inactive


def main():
    print("Checking last sign-in dates for all users...\n")
    report = last_signin_report(days_threshold=90)

    if not report:
        print("No inactive users found.")
        return

    print(f"Users without recent sign-in: {len(report)}\n")
    for u in report[:25]:
        last = u["last_signin"].strftime("%Y-%m-%d") if u["last_signin"] else "Never"
        print(f"  {u['upn']:45s}  {u['display_name'][:25]:25s}  Last: {last}  ({u['days_since']}d ago)")


if __name__ == "__main__":
    main()
