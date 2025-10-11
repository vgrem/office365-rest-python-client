"""
Print users with expired passwords based on password policy
"""

from datetime import datetime, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

users = (
    client.users.select(
        [
            "id",
            "userPrincipalName",
            "displayName",
            "passwordProfile",
            "passwordPolicies",
            "lastPasswordChangeDateTime",
        ]
    )
    .get()
    .filter("accountEnabled eq true")
    .execute_query()
)
expired_count = 0
password_max_age = 90

for user in users:

    password_age = (datetime.now() - user.last_password_change_datetime).days
    must_change_password = password_age >= password_max_age

    if must_change_password:
        expired_days_ago = password_age - password_max_age
        print(f"EXPIRED: {user.user_principal_name} ({user.display_name})")
        print(f"  - Password expired {expired_days_ago} days ago")
        print(f"  - Must change password on next sign-in: {must_change_password}")
        print()
        expired_count += 1

print(f"Found {expired_count} users with expired/forced-change passwords.")
