"""
Audit service principal credentials — list all SPs with their password
and certificate expiry dates for security compliance.

Requires delegated permission ``Application.Read.All``.

https://learn.microsoft.com/en-us/graph/api/serviceprincipal-list
"""

from datetime import datetime, timezone

from office365.directory.password_credential import PasswordCredential
from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

NOW = datetime.now(timezone.utc)
_WARN_DAYS = 30


def _status(cred: PasswordCredential):
    if not cred.endDateTime or cred.endDateTime == datetime.min:
        return "  no_expiry"
    remaining = (cred.endDateTime - NOW).days
    if remaining < 0:
        return f"  expired {abs(remaining)}d ago"
    if remaining < _WARN_DAYS:
        return f"  expires in {remaining}d  <<<"
    return f"  expires in {remaining}d"


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    fields = ["displayName", "appId", "passwordCredentials", "keyCredentials"]
    sps = client.service_principals.select(fields).get().execute_query()

    print(f"Service principal credential audit ({len(sps)} SPs)\n")
    for sp in sorted(sps, key=lambda x: x.display_name or ""):
        if not sp.password_credentials and not sp.key_credentials:
            continue

        print(f"\n  {sp.display_name}  (app_id={sp.app_id})")
        for p in sp.password_credentials:
            print(f"    [P] {p.displayName or '(unnamed)'}{_status(p)}")
        for k in sp.key_credentials:
            print(f"    [C] {k.displayName or '(unnamed)'}{_status(k)}")


if __name__ == "__main__":
    main()
