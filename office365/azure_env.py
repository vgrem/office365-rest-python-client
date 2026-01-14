from enum import Enum
from typing import Dict, Final, TypedDict


class AzureEnvironment(Enum):
    Global = "Global"
    """Referred to as Azure or Azure Global."""

    USGovernment = "GCC"
    """Government Community Cloud"""

    USGovernmentHigh = "GCC High"
    """Government Community Cloud High."""

    China = "CN"
    """Operated by 21Vianet under Chinese regulations."""

    Germany = "Azure DE"
    """Legacy; for data sovereignty in Germany."""

    USGovernmentDoD = "DoD"
    """Azure for U.S. Department of Defense (DoD)"""


class EnvironmentEndpoints(TypedDict):
    graph: str
    login: str


_ENDPOINTS: Final[Dict[AzureEnvironment, EnvironmentEndpoints]] = {
    AzureEnvironment.Global: {
        "graph": "https://graph.microsoft.com",
        "login": "https://login.microsoftonline.com",
    },
    AzureEnvironment.USGovernment: {
        "graph": "https://graph.microsoft.com",
        "login": "https://login.microsoftonline.com",
    },
    AzureEnvironment.USGovernmentHigh: {
        "graph": "https://graph.microsoft.us",
        "login": "https://login.microsoftonline.us",
    },
    AzureEnvironment.USGovernmentDoD: {
        "graph": "https://dod-graph.microsoft.us",
        "login": "https://login.microsoftonline.us",
    },
    AzureEnvironment.Germany: {
        "graph": "https://graph.microsoft.de",
        "login": "https://login.microsoftonline.de",
    },
    AzureEnvironment.China: {
        "graph": "https://microsoftgraph.chinacloudapi.cn",
        "login": "https://login.chinacloudapi.cn",
    },
}


def get_graph_authority(env: AzureEnvironment) -> str:
    """Get the Graph API endpoint for the specified environment.

    Args:
        env: Azure environment enum value

    Returns:
        Graph API endpoint URL

    Example:
        >>> get_graph_authority(AzureEnvironment.Global)
        'https://graph.microsoft.com'
    """
    return _ENDPOINTS.get(env, _ENDPOINTS[AzureEnvironment.Global])["graph"]


def get_login_authority(env: AzureEnvironment) -> str:
    """Get the login endpoint for the specified environment.

    Args:
        env: Azure environment enum value

    Returns:
        Login endpoint URL

    Example:
        >>> get_login_authority(AzureEnvironment.China)
        'https://login.chinacloudapi.cn'
    """
    return _ENDPOINTS.get(env, _ENDPOINTS[AzureEnvironment.Global])["login"]
