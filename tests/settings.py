"""Test/example configuration — reads the environment and a ``.env`` file.

Credentials are centralized here and shared by the integration tests **and** the
runnable examples. They are grouped by authentication flow, using Microsoft's
vocabulary: *delegated access* vs. *app-only access*.

    delegated        delegated access, interactive/device sign-in (tenant + client id)
    delegated-ropc   delegated access via ROPC (adds username + password)
    app-only         app-only access via client secret
    app-only-cert    app-only access via certificate (Entra ID App-Only)

Get started::

    cp .env.example .env        # fill in the blocks you need
    python -m tests.doctor      # show what is ready / missing
    python -m tests.doctor --require app-only-cert   # fail fast in scripts/CI

Missing values are empty strings — never a magic sentinel. Call
``settings.require(flow)`` to fail with an actionable message, or inspect
``settings.missing_for(flow)`` / ``settings.is_ready(flow)``.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
_TEST_DIR = Path(__file__).resolve().parent
_DEFAULT_CERT_PATH = str(_TEST_DIR / "selfsigncert.pem")

#: Environment variable backing each :class:`Settings` field used for readiness.
_ENV = {
    "tenant": "OFFICE365_TENANT",
    "client_id": "OFFICE365_CLIENT_ID",
    "client_secret": "OFFICE365_CLIENT_SECRET",
    "username": "OFFICE365_USERNAME",
    "password": "OFFICE365_PASSWORD",
    "cert_thumbprint": "OFFICE365_CERT_THUMBPRINT",
}


class Flow(NamedTuple):
    """A named authentication flow and the :class:`Settings` fields it needs."""

    label: str
    requires: tuple[str, ...]


#: Authentication flows. Names follow the Microsoft identity platform's
#: "delegated access" / "app-only access" terminology
#: (https://learn.microsoft.com/graph/auth/auth-concepts) and SharePoint's
#: "Entra ID App-Only" model
#: (https://learn.microsoft.com/sharepoint/dev/solution-guidance/security-apponly-azuread).
FLOWS: dict[str, Flow] = {
    "delegated": Flow(
        "Delegated access (interactive / device code / custom)",
        ("tenant", "client_id"),
    ),
    "delegated-ropc": Flow(
        "Delegated access (ROPC username + password)",
        ("tenant", "client_id", "username", "password"),
    ),
    "app-only": Flow(
        "App-only access (client secret)",
        ("tenant", "client_id", "client_secret"),
    ),
    "app-only-cert": Flow(
        "App-only access (certificate / Entra ID App-Only)",
        ("tenant", "client_id", "cert_thumbprint"),
    ),
}


def _unquote(value: str) -> str:
    if value[:1] in ("'", '"') and value[:1] == value[-1:]:
        return value[1:-1]
    return value


def _load_dotenv(path: Path) -> None:
    """Populate ``os.environ`` from a ``.env`` file.

    Real environment variables always win. Supports ``export KEY=value``,
    quoted values and trailing ``# comments``.
    """
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].lstrip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip()
        if value[:1] not in ("'", '"'):
            value = value.split(" #", 1)[0].rstrip()
        os.environ.setdefault(key.strip(), _unquote(value))


def _optional(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


class CredentialsNotConfigured(RuntimeError):
    """Raised when a flow is used while its credentials are not configured."""

    def __init__(self, flow: str, missing: list[str]) -> None:
        self.flow = flow
        self.missing = missing
        super().__init__(
            f"The '{flow}' credentials are not configured. Missing: {', '.join(missing)}.\n"
            "Copy .env.example to .env and fill in the values, then verify with "
            "`python -m tests.doctor`. See README-dev.md for details."
        )


@dataclass(frozen=True)
class Settings:
    """Resolved test/example configuration plus per-flow readiness checks."""

    tenant: str = ""
    client_id: str = ""
    client_secret: str = ""
    username: str = ""
    password: str = ""
    cert_thumbprint: str = ""
    cert_path: str = _DEFAULT_CERT_PATH
    tenant_prefix: str = ""
    root_site_url: str = ""
    site_url: str = ""
    team_site_url: str = ""
    admin_site_url: str = ""
    content_type_hub_url: str = ""
    user_principal: str = ""
    user_principal_alt: str = ""
    admin_username: str = ""
    shared_mailbox_upn: str = ""

    @classmethod
    def from_env(cls) -> Settings:
        tenant = _optional("OFFICE365_TENANT")
        prefix = _optional("OFFICE365_TENANT_PREFIX", tenant.split(".")[0] if tenant else "")
        root_site_url = _optional("OFFICE365_ROOT_SITE_URL", f"https://{prefix}.sharepoint.com" if prefix else "")
        return cls(
            tenant=tenant,
            client_id=_optional("OFFICE365_CLIENT_ID"),
            client_secret=_optional("OFFICE365_CLIENT_SECRET"),
            username=_optional("OFFICE365_USERNAME"),
            password=_optional("OFFICE365_PASSWORD"),
            cert_thumbprint=_optional("OFFICE365_CERT_THUMBPRINT"),
            cert_path=_optional("OFFICE365_CERT_PATH", _DEFAULT_CERT_PATH),
            tenant_prefix=prefix,
            root_site_url=root_site_url,
            site_url=_optional("OFFICE365_SITE_URL", root_site_url),
            team_site_url=_optional("OFFICE365_TEAM_SITE_URL", f"{root_site_url}/sites/team" if root_site_url else ""),
            admin_site_url=_optional(
                "OFFICE365_ADMIN_SITE_URL", f"https://{prefix}-admin.sharepoint.com" if prefix else ""
            ),
            content_type_hub_url=_optional(
                "OFFICE365_CONTENT_TYPE_HUB_URL", f"{root_site_url}/sites/contentTypeHub" if root_site_url else ""
            ),
            user_principal=_optional("OFFICE365_USERNAME"),
            user_principal_alt=_optional("OFFICE365_USERNAME_ALT"),
            admin_username=_optional("OFFICE365_ADMIN_USERNAME"),
            shared_mailbox_upn=_optional("OFFICE365_SHARED_MAILBOX_UPN"),
        )

    def missing_for(self, flow: str) -> list[str]:
        """Return the environment variables / files ``flow`` still needs.

        An empty list means the flow is ready to run.
        """
        if flow not in FLOWS:
            raise ValueError(f"Unknown auth flow: {flow!r} (expected one of {', '.join(FLOWS)})")

        requires = FLOWS[flow].requires
        missing = [_ENV[field] for field in requires if not getattr(self, field)]
        if "cert_thumbprint" in requires and not Path(self.cert_path).is_file():
            missing.append(self.cert_path)
        return missing

    def is_ready(self, flow: str) -> bool:
        """Whether every credential required by ``flow`` is present."""
        return not self.missing_for(flow)

    def readiness(self) -> dict[str, list[str]]:
        """Missing requirements for every flow, computed once."""
        return {flow: self.missing_for(flow) for flow in FLOWS}

    def require(self, flow: str) -> None:
        """Raise :class:`CredentialsNotConfigured` when ``flow`` is not ready."""
        missing = self.missing_for(flow)
        if missing:
            raise CredentialsNotConfigured(flow, missing)


_load_dotenv(PROJECT_ROOT / ".env")
settings = Settings.from_env()

# Backwards-compatible module-level aliases (imported by tests and examples).
tenant = settings.tenant
client_id = settings.client_id
client_secret = settings.client_secret
username = settings.username
password = settings.password
tenant_prefix = settings.tenant_prefix
root_site_url = settings.root_site_url
site_url = settings.site_url
team_site_url = settings.team_site_url
admin_site_url = settings.admin_site_url
content_type_hub_url = settings.content_type_hub_url
cert_thumbprint = settings.cert_thumbprint
cert_path = settings.cert_path
user_principal = settings.user_principal
user_principal_alt = settings.user_principal_alt
admin_username = settings.admin_username
shared_mailbox_upn = settings.shared_mailbox_upn
