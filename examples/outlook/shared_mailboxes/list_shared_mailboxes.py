"""
List shared mailboxes in the tenant.

Graph has no direct "list shared mailboxes" endpoint, so this uses the
common convention that a shared mailbox sets ``onPremisesExtensionAttributes``
``extensionAttribute1`` to "Shared Mailbox". If that attribute isn't
maintained in your tenant, fall back to a UPN-prefix convention (see the
commented alternative). Exchange Online (Get-Mailbox) is the authoritative
source.

Requires delegated or app permission ``User.Read.All``.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

shared = (
    client.users.filter("onPremisesExtensionAttributes/extensionAttribute1 eq 'Shared Mailbox'")
    .select(["id", "displayName", "userPrincipalName", "mail"])
    .get()
    .execute_query()
)
# Alternative when extensionAttribute1 isn't maintained:
#   client.users.filter("startswith(userPrincipalName, 'shared')")...

print(f"Shared mailboxes: {len(shared)}")
for m in shared:
    print(f"  {m.user_principal_name:50s}  {m.display_name}")
