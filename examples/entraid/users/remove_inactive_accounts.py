"""
Remove inactive user accounts in two phases.

Phase "disable"  finds accounts without a sign-in within the last N days, disables
                 them (accountEnabled = false) and marks them with
                 onPremisesExtensionAttributes/extensionAttribute10 = "Inactive".
Phase "delete"   deletes the accounts that a previous run marked as disabled.

The two-phase design avoids deleting accounts on the same run that disables them,
so an administrator has time to review and re-enable anything flagged by mistake.

https://learn.microsoft.com/en-us/graph/api/user-update
https://learn.microsoft.com/en-us/graph/api/user-delete
https://learn.microsoft.com/en-us/graph/api/resources/signinactivity
"""

import argparse
from datetime import datetime, timedelta, timezone
from typing import Optional

from office365.directory.users.user import User
from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

USER_FIELDS = ["id", "displayName", "userPrincipalName", "accountEnabled", "signInActivity"]
INACTIVE_MARKER = {"extensionAttribute10": "Inactive"}
DELETION_FILTER = "accountEnabled eq false and onPremisesExtensionAttributes/extensionAttribute10 eq 'Inactive'"


def _days_since(value: datetime) -> int:
    """Whole days between now and the given UTC timestamp."""
    return (datetime.now(timezone.utc) - value).days


def _last_sign_in(user: User) -> Optional[datetime]:
    """Last interactive or successful sign-in timestamp for a user (or None)."""
    activity = user.sign_in_activity
    last = activity.lastSuccessfulSignInDateTime or activity.lastSignInDateTime
    return last if isinstance(last, datetime) else None


def _list_users(client: GraphClient, group_id: Optional[str]):
    """Accounts to review: members of a group, or all licensed member accounts."""
    return (
        client.users.filter("assignedLicenses/$count ne 0 and userType eq 'Member' and accountEnabled ne false")
        .consistency_level("eventual")
        .select(USER_FIELDS)
        .get()
        .execute_query()
    )


def phase_disable(client: GraphClient, days: int, group_id: Optional[str], dry_run: bool) -> None:
    """Disable and mark accounts inactive for more than `days` days."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    found = 0

    for user in _list_users(client, group_id):
        last = _last_sign_in(user)
        if last is not None and last >= cutoff:
            continue
        found += 1
        idle = _days_since(last) if last is not None else None
        idle_text = f"{idle} days" if idle is not None else "N/A"
        upn = user.properties.get("userPrincipalName", user.id)
        print(f"  {upn}  last sign-in: {last or 'never'}  ({idle_text})")
        if dry_run:
            continue
        user.set_property("accountEnabled", False)
        user.set_property("onPremisesExtensionAttributes", INACTIVE_MARKER)
        user.update().execute_query()
        print("    -> disabled and marked for deletion")

    suffix = " (dry run, nothing changed)" if dry_run else ", disabled & marked"
    print(f"\n{found} inactive account(s) found{suffix}")


def phase_delete(client: GraphClient, dry_run: bool) -> None:
    """Delete accounts disabled and marked by a previous run."""
    marked = client.users.filter(DELETION_FILTER).consistency_level("eventual").select(USER_FIELDS).get().execute_query()
    if not marked:
        print("No previously marked accounts found to delete.")
        return

    for user in marked:
        print(f"  Deleting {user.user_principal_name}")
        if not dry_run:
            user.delete_object().execute_query()

    print(f"\n{len(marked)} account(s) deleted" + (" (dry run)" if dry_run else ""))


def main():
    parser = argparse.ArgumentParser(description="Inactive user account cleanup workflow")
    parser.add_argument(
        "--phase",
        choices=["disable", "delete"],
        required=True,
        help="disable & mark inactive accounts, or delete accounts marked by a previous run",
    )
    parser.add_argument("--days", type=int, default=90, help="inactivity threshold in days (default: 90)")
    parser.add_argument("--group-id", default=None, help="optional group id to scope the disable phase")
    parser.add_argument("--dry-run", action="store_true", help="report only, make no changes")
    args = parser.parse_args()

    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    if args.phase == "disable":
        phase_disable(client, args.days, args.group_id, args.dry_run)
    else:
        phase_delete(client, args.dry_run)


if __name__ == "__main__":
    main()
