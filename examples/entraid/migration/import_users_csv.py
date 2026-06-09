"""
Import users from CSV — bulk provision users from a structured file.

Reads a CSV with user properties and creates each user in Entra ID.
Useful for:
  - Tenant-to-tenant migration user provisioning
  - HR system integration (new hire provisioning)
  - Bulk user creation for testing or staging environments

CSV format:
    userPrincipalName,givenName,surname,displayName,department,jobTitle,
    officeLocation,city,country,mobilePhone,mail,password,accountEnabled

Requires delegated permission ``User.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/user-post-users
"""

import csv
import sys
from io import StringIO

from office365.graph_client import GraphClient
from tests import create_unique_name, test_client_id, test_client_secret, test_tenant

SAMPLE_CSV = """userPrincipalName,givenName,surname,displayName,department,jobTitle,officeLocation,city,country,mobilePhone,mail,password,accountEnabled
user1@contoso.com,John,Doe,John Doe,Engineering,Developer,Seattle,Seattle,USA,+1-555-0101,,TempP@ss123,True
user2@contoso.com,Jane,Smith,Jane Smith,Marketing,Manager,New York,New York,USA,+1-555-0102,,TempP@ss456,True
user3@contoso.com,Bob,Johnson,Bob Johnson,Sales,Representative,Chicago,Chicago,USA,+1-555-0103,,TempP@ss789,True
"""


def import_users_from_csv(csv_content: str) -> list[dict]:
    """Import users from CSV content.

    Returns list of result dicts with status per user.
    """
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
    reader = csv.DictReader(StringIO(csv_content))
    results = []

    for row in reader:
        upn = row["userPrincipalName"].strip()
        password = row.get("password", "").strip() or create_unique_name("P@ssw0rd")

        try:
            # Build user profile
            user = client.users.add_with_password(
                userPrincipalName=upn,
                givenName=row.get("givenName", "").strip(),
                surname=row.get("surname", "").strip(),
                displayName=row.get("displayName", "").strip() or row.get("givenName", "").strip(),
                department=row.get("department", "").strip(),
                jobTitle=row.get("jobTitle", "").strip(),
                officeLocation=row.get("officeLocation", "").strip(),
                city=row.get("city", "").strip(),
                country=row.get("country", "").strip(),
                mobilePhone=row.get("mobilePhone", "").strip(),
                mail=row.get("mail", "").strip() or upn,
                password=password,
                accountEnabled=row.get("accountEnabled", "True").strip().lower() == "true",
            ).execute_query()

            results.append({"user": upn, "status": "success", "id": user.id})
        except Exception as e:
            results.append({"user": upn, "status": "failed", "error": str(e)})

    return results


def main():
    print("Importing users from CSV\n")

    # In production, read from a file:
    # with open("users.csv") as f:
    #     csv_content = f.read()
    csv_content = SAMPLE_CSV

    results = import_users_from_csv(csv_content)

    success = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] == "failed"]

    print(f"Total:   {len(results)}")
    print(f"Created: {len(success)}")
    print(f"Failed:  {len(failed)}\n")

    for r in failed:
        print(f"  ✗ {r['user']}: {r.get('error', 'Unknown')}")

    for r in success:
        print(f"  ✓ {r['user']}  (id: {r['id'][:20]}...)")


if __name__ == "__main__":
    main()
