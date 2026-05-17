from typing import Optional

from office365.runtime.client_value import ClientValue


class TenantAppInformation(ClientValue):
    """Specifies the information for the tenant-scoped app."""

    def __init__(
        self,
        app_principal_id=None,
        app_web_full_url=None,
        creation_time=None,
        icon_absolute_url: Optional[str] = None,
        icon_fallback_absolute_url: Optional[str] = None,
        id_: Optional[str] = None,
        launch_url: Optional[str] = None,
        package_fingerprint: Optional[bytes] = None,
        product_id: Optional[str] = None,
        remote_app_url: Optional[str] = None,
        status: Optional[int] = None,
        title: Optional[str] = None,
    ):
        """
        :param str app_principal_id: Specifies the OAuth Id for the tenant-scoped app.
        :param str app_web_full_url: Specifies the web full URL for the tenant-scoped app.
        :param datetime.datetime creation_time: Specifies the creation time for the tenant-scoped app.
        """
        self.AppPrincipalId = app_principal_id
        self.AppWebFullUrl = app_web_full_url
        self.CreationTime = creation_time
        self.IconAbsoluteUrl = icon_absolute_url
        self.IconFallbackAbsoluteUrl = icon_fallback_absolute_url
        self.Id = id_
        self.LaunchUrl = launch_url
        self.PackageFingerprint = package_fingerprint
        self.ProductId = product_id
        self.RemoteAppUrl = remote_app_url
        self.Status = status
        self.Title = title
