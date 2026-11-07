"""
Read the Exchange organisation configuration and the first ten mailboxes.

App-only: the app signs in for the Exchange audience and every call goes to
``outlook.office365.com/adminapi``. Nothing here writes.

Reaching that API takes two grants - the application permission ``Exchange.ManageAsAppV2`` and a
directory role on the app's service principal. ``exchange_permissions.py`` makes them; this
script only reads.

Set ``OFFICE365_TENANT``, ``OFFICE365_CLIENT_ID`` and ``OFFICE365_CLIENT_SECRET`` in ``.env``.

Requires the application permission ``Exchange.ManageAsAppV2`` and a directory role on the app's
service principal. Run ``exchange_permissions.py`` once if a call answers 403.
"""

from __future__ import annotations

from itertools import islice

from office365.exchange import ExchangeAdminClient
from tests.settings import client_id, client_secret, tenant


def main() -> None:
    client = ExchangeAdminClient(tenant).with_client_secret(client_id, client_secret)

    config = client.get_organization_config().execute_query().value
    print(f"Organisation: {config.get('Name')} (Id: {config.get('Id')})")
    external = "on" if config.get("MailTipsExternalRecipientsTipsEnabled") else "off"
    print(f"Mail tips to external recipients: {external}")
    print(f"Large audience threshold: {config.get('MailTipsLargeAudienceThreshold')}")

    print("\nFirst ten mailboxes:")
    for mailbox in islice(client.get_mailboxes(select=["DisplayName", "PrimarySmtpAddress"]), 10):
        print(f"  {mailbox.get('DisplayName', '?'):35s} {mailbox.get('PrimarySmtpAddress', '')}")


if __name__ == "__main__":
    main()
