"""Setup certificate auth for a SharePoint site.

Generates tests/selfsigncert.{crt,pem}, uploads to app registration,
grants Sites.Selected, prints connection details.

Assumes the app already has the ``Sites.Selected`` application permission with
admin consent. For the full setup cycle — register/reuse the app, grant that
permission, and write ``.env`` — use
``examples/sharepoint/getting-started/setup_sharepoint_app.py``.

Usage: python setup/certificate_auth.py --site <url>
"""

import argparse
import subprocess
from pathlib import Path

from office365.graph_client import GraphClient
from tests.settings import admin_username, client_id, tenant

TEST_DIR = Path(__file__).resolve().parents[4] / "tests"
CERT_PUBLIC = TEST_DIR / "selfsigncert.crt"
CERT_PRIVATE = TEST_DIR / "selfsigncert.pem"


def generate_certificate(common_name: str) -> None:
    TEST_DIR.mkdir(parents=True, exist_ok=True)
    subprocess.run(["openssl", "genrsa", "-out", str(CERT_PRIVATE), "2048"], check=True)
    subprocess.run(
        [
            "openssl",
            "req",
            "-x509",
            "-new",
            "-key",
            str(CERT_PRIVATE),
            "-out",
            str(CERT_PUBLIC),
            "-days",
            "365",
            "-subj",
            f"/CN={common_name}",
        ],
        check=True,
    )


def upload_certificate(client: GraphClient, display_name: str) -> None:
    app = client.applications.get_by_app_id(client_id)
    with open(CERT_PUBLIC, "rb") as f:
        app.add_certificate(f.read(), display_name).execute_query()


def grant_site_access(client: GraphClient, site_url: str) -> None:
    site = client.sites.get_by_url(site_url).execute_query()
    site.grant_app_access(client_id, "write").execute_query()


def get_thumbprint() -> str:
    result = subprocess.run(
        ["openssl", "x509", "-in", str(CERT_PUBLIC), "-noout", "-fingerprint", "-sha1"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip().removeprefix("SHA1 Fingerprint=").replace(":", "")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True)
    parser.add_argument("--name", default="sharepoint-app")
    args = parser.parse_args()

    client = (
        GraphClient(tenant=tenant)
        .with_token_interactive(client_id, admin_username)
        .require_role("Global Administrator", "Privileged Role Administrator")
    )

    generate_certificate(args.name)
    upload_certificate(client, args.name)
    grant_site_access(client, args.site)

    thumbprint = get_thumbprint()
    print(f"Certificate:  {CERT_PUBLIC}")
    print(f"Private key:  {CERT_PRIVATE}")
    print()
    print("Add to .env:")
    print(f"OFFICE365_TENANT={tenant}")
    print(f"OFFICE365_CLIENT_ID={client_id}")
    print(f"OFFICE365_CERT_THUMBPRINT={thumbprint}")


if __name__ == "__main__":
    main()
