import os

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.files.file import File
from office365.sharepoint.marketplace.app_metadata import CorporateCatalogAppMetadata
from office365.sharepoint.marketplace.app_metadata_collection import (
    CorporateCatalogAppMetadataCollection,
)
from office365.sharepoint.marketplace.corporatecuratedgallery.app_request_information import (
    SPStoreAppRequestInformation,
)
from office365.sharepoint.marketplace.corporatecuratedgallery.app_response_information import (
    SPStoreAppResponseInformation,
)
from office365.sharepoint.marketplace.corporatecuratedgallery.app_upgrade_availability import (
    AppUpgradeAvailability,
)
from office365.sharepoint.marketplace.corporatecuratedgallery.card_designs import (
    CardDesigns,
)
from office365.sharepoint.marketplace.corporatecuratedgallery.teams_package_download import (
    TeamsPackageDownload,
)
from office365.sharepoint.marketplace.sitecollection.appcatalog.allowed_items import (
    SiteCollectionAppCatalogAllowedItems,
)


class TenantCorporateCatalogAccessor(Entity):
    """Accessor for the tenant corporate catalog."""

    def add(self, content: bytes, overwrite: bool, url: str = None) -> File:
        """
        Adds a file to the corporate catalog.

        :param str or bytes content: Specifies the binary content of the file to be added.
        :param bool overwrite: Specifies whether to overwrite an existing file with the same name and in the same
            location as the one being added.
        :param str url: Specifies the URL of the file to be added.
        """
        return_type = File(self.context)
        params = {"Overwrite": overwrite, "Url": url}
        qry = ServiceOperationQuery(self, "Add", params, content, None, return_type)
        self.context.add_query(qry)
        return return_type

    def app_from_path(self, path: str, overwrite: bool) -> File:
        """
        Adds a file to the corporate catalog.
        """
        with open(path, "rb") as f:
            content = f.read()
        url = os.path.basename(path)
        return self.add(content=content, overwrite=overwrite, url=url)

    def app_requests(self) -> ClientResult[SPStoreAppResponseInformation]:
        """"""
        return_type = ClientResult(self.context, SPStoreAppResponseInformation())
        payload = {"AppRequestInfo": SPStoreAppRequestInformation()}
        qry = ServiceOperationQuery(
            self, "AppRequests", None, payload, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def download_teams_solution(self, id_: int) -> TeamsPackageDownload:
        """
        Downloads a Microsoft Teams solution package associated with an app from the SharePoint App Catalog
        :param int id_:
        """
        return_type = TeamsPackageDownload(self.context)
        payload = {"id": id_}
        qry = ServiceOperationQuery(
            self, "DownloadTeamsSolution", None, payload, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def get_app_by_id(self, item_unique_id: str) -> CorporateCatalogAppMetadata:
        """
        :param str item_unique_id:
        """
        params = {"itemUniqueId": item_unique_id}
        return CorporateCatalogAppMetadata(
            self.context, ServiceOperationPath("GetAppById", params, self.resource_path)
        )

    def is_app_upgrade_available(
        self, id_: int
    ) -> ClientResult[AppUpgradeAvailability]:
        """
        Determines if an upgrade is available for an app in the SharePoint app catalog
        :param int id_:
        """
        return_type = ClientResult(self.context, AppUpgradeAvailability())
        payload = {"id": id_}
        qry = ServiceOperationQuery(
            self, "IsAppUpgradeAvailable", None, payload, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def upload(self, content, overwrite, url, xor_hash=None):
        """"""
        payload = {
            "Content": content,
            "Overwrite": overwrite,
            "Url": url,
            "XorHash": xor_hash,
        }
        qry = ServiceOperationQuery(self, "Upload", None, payload)
        self.context.add_query(qry)
        return self

    def send_app_request_status_notification_email(self, request_guid: str) -> Self:
        """
        Sends email notifications about the status of an app request in the corporate app catalog
        :param str request_guid:
        """
        qry = ServiceOperationQuery(
            self, "SendAppRequestStatusNotificationEmail", [request_guid]
        )
        self.context.add_query(qry)
        return self

    @property
    def available_apps(self) -> CorporateCatalogAppMetadataCollection:
        """Returns the apps available in this corporate catalog."""
        return self.properties.get(
            "AvailableApps",
            CorporateCatalogAppMetadataCollection(
                self.context, ResourcePath("AvailableApps", self.resource_path)
            ),
        )

    @property
    def card_designs(self) -> CardDesigns:
        """Returns the card designs available in this corporate catalog."""
        return self.properties.get(
            "CardDesigns",
            CardDesigns(self.context, ResourcePath("CardDesigns", self.resource_path)),
        )

    @property
    def site_collection_app_catalogs_sites(
        self,
    ) -> SiteCollectionAppCatalogAllowedItems:
        """Returns an accessor to the allow list of site collections allowed to have site collection corporate
        catalogs."""
        return self.properties.get(
            "SiteCollectionAppCatalogsSites",
            SiteCollectionAppCatalogAllowedItems(
                self.context,
                ResourcePath("SiteCollectionAppCatalogsSites", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.TenantCorporateCatalogAccessor"

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "AvailableApps": self.available_apps,
                "CardDesigns": self.card_designs,
                "SiteCollectionAppCatalogsSites": self.site_collection_app_catalogs_sites,
            }
            default_value = property_mapping.get(name, None)
        return super().get_property(name, default_value)
