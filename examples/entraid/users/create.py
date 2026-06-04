"""
Create a user.

Creates a new user in the tenant with a display name, user principal name,
and a temporary password that must be changed on first sign-in.

https://learn.microsoft.com/en-us/graph/api/user-post-users

https://learn.microsoft.com/en-us/graph/api/resources/user

Requires delegated permission ``User.ReadWrite.All``.
"""

from office365.directory.users.password_profile import PasswordProfile
from office365.directory.users.profile import UserProfile
from office365.graph_client import GraphClient
from tests import (
    create_unique_name,
    test_client_id,
    test_password,
    test_tenant,
    test_username,
)

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

profile = UserProfile(
    displayName=create_unique_name("NewUser"),
    userPrincipalName=f"{create_unique_name('user')}@{test_tenant}",
    mailNickname=create_unique_name("user"),
    accountEnabled=True,
    passwordProfile=PasswordProfile(
        password=create_unique_name("P@ssw0rd"),
        forceChangePasswordNextSignIn=True,
    ),
)

user = client.users.add(profile).execute_query()
print(f"User created: {user.display_name} ({user.user_principal_name})")

# clean up
user.delete_object(True).execute_query()
print("User cleaned up.")
