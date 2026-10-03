"""
Add (or generate) a certificate for an app using Microsoft Graph.

Uploads the *public* certificate (``.crt``/``.cer``); the private key stays local
and is what the client authenticates with (``OFFICE365_CERT_PATH``).

Pass ``--generate`` to create a self-signed pair with openssl first and print a
paste-ready ``.env`` block. Otherwise ``--cert`` uploads an existing certificate.

https://learn.microsoft.com/en-us/graph/applications-how-to-add-certificate

Requires delegated permission ``Application.ReadWrite.All``.
"""

import argparse
import subprocess
from pathlib import Path

from office365.graph_client import GraphClient
from tests.settings import admin_username, client_id, tenant

DEFAULT_CERT = "tests/selfsigncert.crt"


def generate_certificate(cert_path: Path, key_path: Path, common_name: str) -> None:
    cert_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["openssl", "genrsa", "-out", str(key_path), "2048"], check=True)
    subprocess.run(
        [
            "openssl",
            "req",
            "-x509",
            "-new",
            "-key",
            str(key_path),
            "-out",
            str(cert_path),
            "-days",
            "365",
            "-subj",
            f"/CN={common_name}",
        ],
        check=True,
    )


def get_thumbprint(cert_path: Path) -> str:
    result = subprocess.run(
        ["openssl", "x509", "-in", str(cert_path), "-noout", "-fingerprint", "-sha1"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip().removeprefix("SHA1 Fingerprint=").replace(":", "")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cert", default=DEFAULT_CERT, help="path to the public certificate (default: %(default)s)")
    parser.add_argument("--name", default="office365-rest-python-client", help="certificate display name")
    parser.add_argument("--generate", action="store_true", help="generate a self-signed certificate first")
    args = parser.parse_args()

    cert_path = Path(args.cert)
    key_path = cert_path.with_suffix(".pem")

    if args.generate:
        generate_certificate(cert_path, key_path, args.name)

    client = (
        GraphClient(tenant=tenant)
        .with_token_interactive(client_id, admin_username)
        .require_role("Global Administrator", "Privileged Role Administrator")
    )

    target_app = client.applications.get_by_app_id(client_id)
    target_app.add_certificate(cert_path.read_bytes(), args.name).execute_query()
    print(f"Uploaded {cert_path} to app {client_id}")

    if args.generate:
        print()
        print("Add to .env:")
        print(f"OFFICE365_TENANT={tenant}")
        print(f"OFFICE365_CLIENT_ID={client_id}")
        print(f"OFFICE365_CERT_THUMBPRINT={get_thumbprint(cert_path)}")
        print(f"OFFICE365_CERT_PATH={key_path}")


if __name__ == "__main__":
    main()
