"""
Report stale registered devices that haven't been used for sign-in recently.

Requires delegated permission Device.Read.All.
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    cutoff = datetime.now(timezone.utc) - timedelta(days=180)
    stale = []

    for device in client.devices.get().execute_query():
        last = device.approximate_last_signin_datetime
        if last and last < cutoff:
            stale.append(
                (
                    device.display_name or "Unnamed",
                    device.operating_system or "Unknown",
                    last,
                )
            )

    stale.sort(key=lambda x: x[2])
    print(f"Stale devices (180+ days): {len(stale)}")
    for name, os, last in stale:
        print(f"  {name}  {os}  {last.date()}")


if __name__ == "__main__":
    main()
