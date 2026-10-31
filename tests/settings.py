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


# --------------------------------------------------------------------------- #
# .env (the same grammar the setup wizard writes)
# --------------------------------------------------------------------------- #
def _assignment(line: str) -> tuple[str, str] | None:
    """Return ``(key, raw value)`` for an assignment line, ``None`` for anything else."""
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    if stripped.startswith("export "):
        stripped = stripped[len("export ") :].lstrip()
    key, sep, value = stripped.partition("=")
    if not sep:
        return None
    return key.strip(), value


class EnvFile:
    """The ``.env`` file: read it into the environment, merge discoveries back, redact it.

    Two programs write through it — :mod:`tests.settings` at import, :mod:`tests.setup`
    when it has discovered credentials — and they each had a parser before, which
    disagreed about an unquoted ``KEY=value  # note`` (the reader dropped the comment,
    the writer kept it in the value). One grammar:

    * blank and ``#`` lines carry nothing; ``export KEY=value`` is ``KEY=value``;
    * quotes are removed, and a value keeps a trailing ``#`` comment only when quoted;
    * merging replaces a value in place, fills only an empty key, and preserves every
      comment and unrelated key.
    """

    #: Values :meth:`redact` replaces before the wizard prints anything.
    secrets: tuple[str, ...] = ("OFFICE365_CLIENT_SECRET", "OFFICE365_PASSWORD")

    def __init__(self, path: Path, example: Path | None = None) -> None:
        self.path = path
        self.example = example

    @staticmethod
    def _parse(text: str) -> dict[str, str]:
        values: dict[str, str] = {}
        for line in text.splitlines():
            entry = _assignment(line)
            if entry is None:
                continue
            key, value = entry
            value = value.strip()
            if value[:1] not in ("'", '"'):
                value = value.split(" #", maxsplit=1)[0].rstrip()
            values[key] = value[1:-1] if value[:1] in ("'", '"') and value[:1] == value[-1:] else value
        return values

    def read(self) -> dict[str, str]:
        """The values the file sets, or nothing when it does not exist (a fresh checkout)."""
        if not self.path.is_file():
            return {}
        return self._parse(self.path.read_text(encoding="utf-8-sig"))

    def load(self) -> None:
        """Populate ``os.environ``; a real environment variable always wins."""
        for key, value in self.read().items():
            os.environ.setdefault(key, value)

    def source_lines(self) -> list[str]:
        """The lines to edit: the file when it exists, else the commented template."""
        for candidate in (self.path, self.example):
            if candidate is not None and candidate.is_file():
                return candidate.read_text(encoding="utf-8-sig").splitlines()
        return []

    def merge(self, overrides: dict[str, str], defaults: dict[str, str]) -> str:
        """Return the file's text with ``overrides`` set and missing ``defaults`` filled."""
        pending = dict(overrides)
        fill = dict(defaults)
        output: list[str] = []
        for line in self.source_lines():
            entry = _assignment(line)
            if entry is not None:
                key, current = entry
                if key in pending:
                    output.append(f"{key}={pending.pop(key)}")
                    continue
                if key in fill:
                    fallback = fill.pop(key)
                    if not current.strip():
                        output.append(f"{key}={fallback}")
                        continue
            output.append(line)
        tail = {**fill, **pending}
        if tail:
            output += ["", "# Added by python -m tests.setup"]
            output += [f"{key}={value}" for key, value in tail.items()]
        return "\n".join(output).rstrip() + "\n"

    def redact(self, text: str) -> str:
        """Return ``text`` with the values of :attr:`secrets` replaced by ``<hidden>``."""
        output: list[str] = []
        for line in text.splitlines():
            entry = _assignment(line)
            output.append(f"{entry[0]}=<hidden>" if entry is not None and entry[0] in self.secrets else line)
        return "\n".join(output)


#: The repository's ``.env``, and the commented template that stands in for it.
ENV = EnvFile(PROJECT_ROOT / ".env", PROJECT_ROOT / ".env.example")

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


def _optional(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def _url(key: str, derived: dict[str, str]) -> str:
    """A URL from the environment, falling back to the tenant-derived default."""
    return _optional(key, derived.get(key, ""))


def _resolve_path(value: str) -> str:
    """Resolve a filesystem path for use from any working directory.

    Paths configured in ``.env`` are documented relative to the repository root
    (e.g. ``OFFICE365_CERT_PATH=tests/selfsigncert.pem``), so a relative value is
    anchored to :data:`PROJECT_ROOT` instead of the current working directory.
    Absolute paths and ``~`` are respected as-is.
    """
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return str(path)


def derived_urls(prefix: str, root: str = "") -> dict[str, str]:
    """What a tenant name alone determines about its URLs, keyed by ``.env`` name.

    ``root`` is an already-resolved root site (an ``.env`` that sets only
    ``OFFICE365_ROOT_SITE_URL`` still gets consistent children). The wizard writes
    this dict as the ``.env`` defaults and :meth:`Settings.from_env` reads it as the
    fallback for the same keys, so the shape is stated once.
    """
    root = root or (f"https://{prefix}.sharepoint.com" if prefix else "")
    urls = {"OFFICE365_TENANT_PREFIX": prefix, "OFFICE365_ROOT_SITE_URL": root}
    if root:
        urls |= {
            "OFFICE365_SITE_URL": root,
            "OFFICE365_TEAM_SITE_URL": f"{root}/sites/team",
            "OFFICE365_CONTENT_TYPE_HUB_URL": f"{root}/sites/contentTypeHub",
        }
    if prefix:
        urls["OFFICE365_ADMIN_SITE_URL"] = f"https://{prefix}-admin.sharepoint.com"
    return urls


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
    setup_client_id: str = ""
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
        prefix = _optional("OFFICE365_TENANT_PREFIX", tenant.split(".", maxsplit=1)[0])
        urls = derived_urls(prefix, _optional("OFFICE365_ROOT_SITE_URL"))
        return cls(
            tenant=tenant,
            client_id=_optional("OFFICE365_CLIENT_ID"),
            setup_client_id=_optional("OFFICE365_SETUP_CLIENT_ID"),
            client_secret=_optional("OFFICE365_CLIENT_SECRET"),
            username=_optional("OFFICE365_USERNAME"),
            password=_optional("OFFICE365_PASSWORD"),
            cert_thumbprint=_optional("OFFICE365_CERT_THUMBPRINT"),
            cert_path=_resolve_path(_optional("OFFICE365_CERT_PATH", _DEFAULT_CERT_PATH)),
            tenant_prefix=prefix,
            root_site_url=_url("OFFICE365_ROOT_SITE_URL", urls),
            site_url=_url("OFFICE365_SITE_URL", urls),
            team_site_url=_url("OFFICE365_TEAM_SITE_URL", urls),
            admin_site_url=_url("OFFICE365_ADMIN_SITE_URL", urls),
            content_type_hub_url=_url("OFFICE365_CONTENT_TYPE_HUB_URL", urls),
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

    def format_readiness(self) -> str:
        """A human-readable readiness report for every flow (the doctor/setup banner)."""
        ready = self.readiness()
        width = max(len(spec.label) for spec in FLOWS.values())
        lines = ["Auth readiness (environment + .env):"]
        for flow, spec in FLOWS.items():
            missing = ready[flow]
            detail = "" if not missing else "  missing: " + ", ".join(missing)
            lines.append(f"  {spec.label:<{width}}  {'not ready' if missing else 'ready':<9}{detail}")
        if not any(self.is_ready(flow) for flow in FLOWS):
            lines += ["", "  Tip: run `python -m tests.setup` (or copy .env.example), then re-run `tests.doctor`."]
        return "\n".join(lines)

    def require(self, flow: str) -> None:
        """Raise :class:`CredentialsNotConfigured` when ``flow`` is not ready."""
        missing = self.missing_for(flow)
        if missing:
            raise CredentialsNotConfigured(flow, missing)


ENV.load()
settings = Settings.from_env()


def __getattr__(name: str):
    """The module-level aliases (``tests.settings.site_url`` …) read the settings object.

    One vocabulary: a field added to :class:`Settings` is reachable as
    ``settings.<field>`` and as ``tests.settings.<field>`` without a second list to
    keep in step.
    """
    if name in Settings.__dataclass_fields__:
        return getattr(settings, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
