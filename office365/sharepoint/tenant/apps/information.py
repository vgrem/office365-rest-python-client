from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TenantAppInformation(ClientValue):
    """Specifies the information for the tenant-scoped app.

    Args:
        app_principal_id (str): Specifies the OAuth Id for the tenant-scoped app.
        app_web_full_url (str): Specifies the web full URL for the tenant-scoped app.
        creation_time (datetime.datetime): Specifies the creation time for the tenant-scoped app.
    """

    AppPrincipalId = None
    AppWebFullUrl = None
    CreationTime = None
    IconAbsoluteUrl: str | None = None
    IconFallbackAbsoluteUrl: str | None = None
    Id: str | None = None
    LaunchUrl: str | None = None
    PackageFingerprint: bytes | None = None
    ProductId: str | None = None
    RemoteAppUrl: str | None = None
    Status: int | None = None
    Title: str | None = None
