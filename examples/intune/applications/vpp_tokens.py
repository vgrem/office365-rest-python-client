"""
Apple VPP tokens: list tokens and their sync/expiry status.

Volume Purchase Program (VPP) tokens control Apple volume app licensing.
This lists tokens and flags stale syncs or expiring tokens.

Requires delegated permission ``DeviceManagementApps.Read.All``.

https://learn.microsoft.com/en-us/graph/api/intune-apps-vpptokens-list
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
tokens = client.device_app_management.vpp_tokens.get().execute_query()
print(f"Apple VPP tokens ({len(tokens)}):\n")

threshold = datetime.now(timezone.utc) + timedelta(days=30)
for t in tokens:
    stale = t.last_sync_date_time and t.last_sync_date_time < datetime.now(timezone.utc) - timedelta(days=7)
    expiring = t.expiration_date_time and t.expiration_date_time < threshold
    print(f"  {t.organization_name or '(unnamed)':35s}  [{t.state or '?'}]")
    print(f"    Apple ID: {t.apple_id or '?'}  Account: {t.vpp_token_account_type or '?'}")
    print(f"    Last sync: {t.last_sync_date_time or 'never'}  ({t.last_sync_status or '?'})")
    flags = " ".join(["[STALE]" if stale else "", "[EXPIRING]" if expiring else ""]).strip()
    print(f"    Expires: {t.expiration_date_time or '?'}  {flags}")
    print()
