"""
Report on application certificates and secrets that are expiring soon.

App credentials that expire unexpectedly cause silent outages. This
script identifies apps with expiring secrets/certs so they can be
rotated before they expire.

Inspired by Report-ExpiringAppSecrets.PS1 from Office 365 for IT Pros.

Required delegated permissions:
    Application.Read.All     Read application registrations
    Application.ReadWrite.All  (optional) to renew expiring secrets

https://learn.microsoft.com/en-us/graph/api/resources/application
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def find_expiring_secrets(days_ahead: int = 30) -> list[dict]:
    """Find app secrets and certificates expiring within *days_ahead*.

    Args:
        days_ahead: Alert window — credentials expiring within this
                    many days are flagged.

    Returns:
        List of expiring credential dicts sorted by expiry date.
    """
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    cutoff = datetime.now(timezone.utc) + timedelta(days=days_ahead)
    expiring = []

    apps = client.applications.get().execute_query()

    for app in apps:
        app_name = getattr(app, "display_name", "Unnamed")
        app_id = getattr(app, "app_id", "")

        # Check passwords
        passwords = getattr(app, "password_credentials", [])
        for cred in passwords or []:
            end_date = getattr(cred, "end_date_time", None)
            if end_date and end_date <= cutoff:
                expiring.append(
                    {
                        "app": app_name,
                        "app_id": app_id,
                        "type": "Password",
                        "hint": getattr(cred, "hint", "") or getattr(cred, "display_name", ""),
                        "expires": end_date,
                    }
                )

        # Check certificates
        certs = getattr(app, "key_credentials", [])
        for cred in certs or []:
            end_date = getattr(cred, "end_date_time", None)
            if end_date and end_date <= cutoff:
                expiring.append(
                    {
                        "app": app_name,
                        "app_id": app_id,
                        "type": "Certificate",
                        "hint": getattr(cred, "display_name", "") or getattr(cred, "key_id", ""),
                        "expires": end_date,
                    }
                )

    expiring.sort(key=lambda x: x["expires"])
    return expiring


def main():
    print("Checking for expiring application credentials...\n")
    expiring = find_expiring_secrets(days_ahead=30)

    if not expiring:
        print("No secrets expiring within 30 days. ✓")
        return

    print(f"Found {len(expiring)} credentials expiring within 30 days:\n")
    for c in expiring:
        days = (c["expires"] - datetime.now(timezone.utc)).days
        print(
            f"  {c['app']:35s}  [{c['type']:12s}]  {c['hint'][:25]:25s}"
            f"  Expires: {c['expires'].strftime('%Y-%m-%d')}  ({days}d)"
        )


if __name__ == "__main__":
    main()
