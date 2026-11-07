"""
Read the Exchange organisation configuration, signed in with a certificate.

The same read as ``exchange_admin.py``; only the credential changes. A certificate holds no
shared secret, so it is the flow production daemons use - and the private key never leaves the
machine it runs on.

Set ``OFFICE365_TENANT``, ``OFFICE365_CLIENT_ID`` and ``OFFICE365_CERT_THUMBPRINT`` in ``.env``;
the private key is ``tests/selfsigncert.pem`` unless ``OFFICE365_CERT_PATH`` says otherwise.

Requires the application permission ``Exchange.ManageAsAppV2`` and a directory role on the app's
service principal. Run ``exchange_permissions.py`` once if a call answers 403.
"""

from __future__ import annotations

from pathlib import Path

from office365.exchange import ExchangeAdminClient
from tests.settings import cert_path, cert_thumbprint, client_id, tenant


def main() -> None:
    private_key = Path(cert_path).read_text()  # the certificate's private half, never sent
    client = ExchangeAdminClient(tenant).with_certificate(client_id, cert_thumbprint, private_key)

    config = client.get_organization_config().execute_query().value
    print(f"Signed in with certificate {cert_thumbprint[:16]}...")
    print(f"Organisation: {config.get('Name')} (Id: {config.get('Id')})")


if __name__ == "__main__":
    main()
