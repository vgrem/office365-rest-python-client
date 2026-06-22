"""
Find apps with already-expired client secrets.

A practical response to the AADSTS7000222 error — find every
app registration whose password credentials have passed their
endDateTime so they can be rotated.

Requires delegated permission Application.Read.All.

https://learn.microsoft.com/en-us/graph/api/resources/application
"""

from office365.graph_client import GraphClient
from tests.settings import admin_username, client_id, tenant


def main():
    client = (
        GraphClient(tenant=tenant)
        .with_token_interactive(client_id, admin_username)
        .require_role("Global Administrator", "Privileged Role Administrator")
    )

    expired = []
    for app in client.applications.get().execute_query():
        for cred in app.password_credentials or []:
            if cred.is_expired:
                expired.append((app.display_name or "Unnamed", cred))

    print(f"Apps with expired secrets: {len(expired)}\n")
    for name, cred in expired:
        print(f"  {name}  hint={cred.hint}  expires={cred.endDateTime}")


if __name__ == "__main__":
    main()
