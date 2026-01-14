"""
Reset user password (requires admin privileges)
"""

import getpass
import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant, test_username

confirm2 = input(f"Are you sure you want to reset the password for user '{test_username}'? (yes/NO): ").strip().lower()
if confirm2 not in ["yes", "y"]:
    print("Operation cancelled.")
    sys.exit(0)

print()

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

new_password = getpass.getpass(f"Enter new password for user {test_username}: ").strip()

# Confirm password
confirm_password = getpass.getpass(f"Confirm new password for user {test_username}: ").strip()

if new_password != confirm_password:
    print("Error: Passwords do not match!")
    sys.exit(1)

if not new_password:
    print("Error: Password cannot be empty!")
    sys.exit(1)

force_change = False
user = client.users[test_username]
user.password_profile.password = new_password
user.password_profile.forceChangePasswordNextSignIn = force_change
user.update().execute_query()
print(f"Password reset for user: {test_username}")
print(f"Force change on next login: {force_change}")
