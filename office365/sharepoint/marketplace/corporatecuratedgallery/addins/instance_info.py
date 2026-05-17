from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class SPAddinInstanceInfo(ClientValue):
    def __init__(
        self,
        app_identifier: Optional[str] = None,
        app_instance_id: Optional[str] = None,
        tenant_app_data: Optional[str] = None,
        tenant_app_data_update_time: Optional[datetime] = None,
        title: Optional[str] = None,
        app_source: Optional[str] = None,
        app_web_full_url: Optional[str] = None,
        app_web_id: Optional[str] = None,
        app_web_name: Optional[str] = None,
        asset_id: Optional[str] = None,
        creation_time_utc: Optional[datetime] = None,
        current_site_id: Optional[str] = None,
        current_web_id: Optional[str] = None,
        current_web_name: Optional[str] = None,
        current_web_url: Optional[str] = None,
        installed_by: Optional[str] = None,
        installed_site_id: Optional[str] = None,
        installed_web_id: Optional[str] = None,
        installed_web_name: Optional[str] = None,
        installed_web_url: Optional[str] = None,
        launch_url: Optional[str] = None,
        license_purchase_time: Optional[datetime] = None,
        locale: Optional[str] = None,
        product_id: Optional[str] = None,
        purchaser_identity: Optional[str] = None,
        status: Optional[str] = None,
    ):
        """
        :param str app_identifier:
        :param str app_instance_id:
        :param str tenant_app_data:
        :param datetime.datetime tenant_app_data_update_time:
        :param str title:
        """
        self.appIdentifier = app_identifier
        self.appInstanceId = app_instance_id
        self.tenantAppData = tenant_app_data
        self.tenantAppDataUpdateTime = tenant_app_data_update_time
        self.title = title
        self.appSource = app_source
        self.appWebFullUrl = app_web_full_url
        self.appWebId = app_web_id
        self.appWebName = app_web_name
        self.assetId = asset_id
        self.creationTimeUtc = creation_time_utc
        self.currentSiteId = current_site_id
        self.currentWebId = current_web_id
        self.currentWebName = current_web_name
        self.currentWebUrl = current_web_url
        self.installedBy = installed_by
        self.installedSiteId = installed_site_id
        self.installedWebId = installed_web_id
        self.installedWebName = installed_web_name
        self.installedWebUrl = installed_web_url
        self.launchUrl = launch_url
        self.licensePurchaseTime = license_purchase_time
        self.locale = locale
        self.productId = product_id
        self.purchaserIdentity = purchaser_identity
        self.status = status

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPAddinInstanceInfo"
