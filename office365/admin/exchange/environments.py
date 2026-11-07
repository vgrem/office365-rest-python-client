"""Exchange Online Admin API hosts per cloud (Microsoft Learn: admin-api-get-started, 2026-09)."""

from __future__ import annotations

from office365.azure_env import AzureEnvironment

_HOSTS = {
    AzureEnvironment.Global: "https://outlook.office365.com",
    AzureEnvironment.USGovernment: "https://outlook.office365.com",
    AzureEnvironment.USGovernmentHigh: "https://outlook.office365.us",
    AzureEnvironment.USGovernmentDoD: "https://outlook-dod.office365.us",
    AzureEnvironment.China: "https://outlook.office365.cn",
}

ADMIN_API_VERSION = "v2.0"

#: Same value in every organisation; the routing key for app-only calls with no target mailbox.
SYSTEM_MAILBOX_GUID = "bb558c35-97f1-4cb9-8ff7-d53741dc928c"


def exchange_host(environment: AzureEnvironment) -> str:
    try:
        return _HOSTS[environment]
    except KeyError:
        raise ValueError(f"Exchange Online Admin API is not available for {environment}") from None


def exchange_scope(environment: AzureEnvironment) -> str:
    """The ``.default`` scope of the Exchange audience; a Graph token is rejected with 401."""
    return f"{exchange_host(environment)}/.default"
