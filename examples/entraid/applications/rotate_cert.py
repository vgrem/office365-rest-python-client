"""
Add a certificate to an app using Microsoft Graph.

Uploads the *public* certificate (``.crt``/``.cer``); the private key stays local
and is what the client authenticates with (``OFFICE365_CERT_PATH``).

To create a self-signed pair, run:

    openssl req -x509 -newkey rsa:2048 -keyout selfsignkey.pem -out selfsigncert.crt -nodes -days 365

or let ``examples/sharepoint/auth/setup/certificate_auth.py`` do it end to end.

https://learn.microsoft.com/en-us/graph/applications-how-to-add-certificate

Requires delegated permission ``Application.ReadWrite.All``.
"""

import argparse
from pathlib import Path

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cert",
        default="tests/selfsigncert.crt",
        help="path to the public certificate to upload (default: %(default)s)",
    )
    parser.add_argument("--name", default="office365-rest-python-client", help="certificate display name")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    target_app = client.applications.get_by_app_id(client_id)
    cert_data = Path(args.cert).read_bytes()
    target_app.add_certificate(cert_data, args.name).execute_query()
    print(f"Uploaded {args.cert} to app {client_id}")


if __name__ == "__main__":
    main()
