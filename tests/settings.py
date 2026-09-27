"""Test configuration — reads from environment and .env file.

Mandatory vs optional:
    Mandatory — needed to run integration tests; falls back to ``"x"`` when unset
                so offline collection keeps working (the base test cases treat
                ``"x"`` as "not configured").
    Optional  — derived from tenant when not set, or left empty (skips related tests).
"""

from __future__ import annotations

import os
from pathlib import Path

_PROJECT_ROOT = Path(__file__).parent.parent


def _load_dotenv() -> None:
    dotenv = _PROJECT_ROOT / ".env"
    if dotenv.is_file():
        for raw_line in dotenv.read_text().splitlines():
            line = raw_line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


_load_dotenv()

_MISSING = "x"


def _require(key: str) -> str:
    """Return a value, or the ``"x"`` sentinel when it is unset.

    Missing credentials must not break test collection: the offline unit suite
    runs without a tenant, and the credentialed suites skip via
    ``tests/conftest.py`` (``--offline``) and the ``"x"`` guards in the base
    test cases.
    """
    return os.environ.get(key) or _MISSING


def _optional(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


# Mandatory — must be set for integration tests
tenant = _require("OFFICE365_TENANT")
client_id = _require("OFFICE365_CLIENT_ID")
client_secret = _require("OFFICE365_CLIENT_SECRET")
username = _require("OFFICE365_USERNAME")
password = _require("OFFICE365_PASSWORD")

# Optional — derived from tenant when not set
tenant_prefix = _optional("OFFICE365_TENANT_PREFIX", tenant.split(".")[0])
root_site_url = _optional("OFFICE365_ROOT_SITE_URL", f"https://{tenant_prefix}.sharepoint.com")
site_url = _optional("OFFICE365_SITE_URL", root_site_url)
team_site_url = _optional("OFFICE365_TEAM_SITE_URL", f"https://{tenant_prefix}.sharepoint.com/sites/project")
admin_site_url = _optional("OFFICE365_ADMIN_SITE_URL", f"https://{tenant_prefix}-admin.sharepoint.com")
content_type_hub_url = _optional("OFFICE365_CONTENT_TYPE_HUB_URL", f"{root_site_url}/sites/contentTypeHub")

# Optional — only needed for specific scenarios (empty default = skip)
cert_thumbprint = _optional("OFFICE365_CERT_THUMBPRINT")
user_principal = _optional("OFFICE365_TEST_USER1")
user_principal_alt = _optional("OFFICE365_TEST_USER2")
admin_username = _optional("OFFICE365_ADMIN_USERNAME")
shared_mailbox_upn = _optional("OFFICE365_SHARED_MAILBOX_UPN")

_cert_dir = Path(__file__).parent
cert_path = str(_cert_dir / "selfsigncert.pem")
