"""
Group lifecycle policies — set group expiration, manage renewal,
and enable auto-renewal for Microsoft 365 groups.

M365 group expiration is a core governance feature. Without it,
groups accumulate and never get cleaned up. This example shows:
  - List existing lifecycle policies
  - Add groups to a policy
  - Remove groups from a policy
  - Renew a group (keep alive)

Requires delegated permission ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/resources/grouplifecyclepolicy
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    # -- Step 1: list existing lifecycle policies --
    policies = client.group_lifecycle_policies.get().execute_query()
    print(f"Group lifecycle policies: {len(policies)}\n")

    for p in policies:
        lifetime = p.group_lifetime_in_days or "?"
        notification = p.alternate_notification_emails or "(none)"
        managed = p.managed_group_types or []
        print(f"  Lifetime: {lifetime:>3} days  notification: {notification:45s}  managed types: {managed}")

    # -- Step 2: find groups not covered by any policy --
    groups = (
        client.groups.get()
        .filter("resourceProvisioningOptions/Any(x:x eq 'Team') or mailEnabled eq true")
        .select(["id", "displayName", "mail"])
        .top(999)
        .execute_query()
    )

    covered = set()
    for p in policies:
        gid = p.properties.get("groupId", "")
        if gid:
            covered.add(gid)
        elif hasattr(p, "properties") and p.properties.get("groupIds"):
            for gid in p.properties["groupIds"]:
                covered.add(gid)

    uncovered = [g for g in groups if g.id not in covered]
    print(f"\nM365 groups: {len(groups)}")
    print(f"Uncovered by lifecycle policy: {len(uncovered)}")

    if uncovered:
        print("\nFirst 5 groups without expiration:")
        for g in uncovered[:5]:
            print(f"  {g.display_name:40s}  {g.mail or '?'}")

    # -- Step 3: create a lifecycle policy (commented) --
    # policy = client.group_lifecycle_policies.add(
    #     groupLifetimeInDays=180,
    #     managedGroupTypes="All",
    #     alternateNotificationEmails="admin@contoso.com",
    # ).execute_query()
    # print(f"\n✓ Lifecycle policy created")

    # -- Step 4: add a group to the policy --
    if policies and uncovered:
        policy = policies[0]
        group_id = uncovered[0].id
        policy.add_group(group_id=group_id).execute_query()
        print(f"\n✓ Added {uncovered[0].display_name} to lifecycle policy.")

    # -- Step 5: renew a group (keep alive another period) --
    if policies:
        # Pick any group ID that was already managed
        sample = next((p.properties.get("groupId", "") for p in policies if p.properties.get("groupId")), None)
        if sample:
            policies[0].renew_group(group_id=sample).execute_query()
            print(f"✓ Renewed group {sample[:20]}.")

    # -- Cleanup: remove a group from policy --
    # policy.remove_group(group_id=group_id).execute_query()
    # print("✓ Removed group from policy.")

    print("\nDone.")


if __name__ == "__main__":
    main()
