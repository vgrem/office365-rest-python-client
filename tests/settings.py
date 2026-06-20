"""Test configuration — reads from environment and .env file.

Mandatory vs optional:
    Mandatory — required for any integration test to run.
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


def _require(key: str) -> str:
    val = os.environ.get(key)
    if not val:
        raise RuntimeError(f"{key} is not set. Add it to .env in the project root.")
    return val


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

# Optional — only needed for specific scenarios (empty default = skip)
cert_thumbprint = _optional("OFFICE365_CERT_THUMBPRINT")
test_user1 = _optional("OFFICE365_TEST_USER1")
test_user2 = _optional("OFFICE365_TEST_USER2")
admin_username = _optional("OFFICE365_ADMIN_USERNAME")
