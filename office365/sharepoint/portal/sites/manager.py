from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union
from uuid import UUID

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import GuidCollection
from office365.sharepoint.entity import Entity
from office365.sharepoint.portal.groups.moveoperation import GroupMoveOperation
from office365.sharepoint.portal.sites.creation_request import SPSiteCreationRequest
from office365.sharepoint.portal.sites.creation_response import SPSiteCreationResponse
from office365.sharepoint.teams.site_owner_response import GetTeamChannelSiteOwnerResponse
from office365.sharepoint.tenant.administration.ibsegmentinfo import IBSegmentInfo
from office365.sharepoint.viva.site_request_info import VivaSiteRequestInfo

if TYPE_CHECKING:
    from office365.sharepoint.principal.users.user import User


class SPSiteManager(Entity):
    """Provides REST methods for creating and managing SharePoint sites."""

    def __init__(self, context, resource_path=None):
        if resource_path is None:
            resource_path = ResourcePath("SPSiteManager")
        super().__init__(context, resource_path)

    def create(
        self, title: str, site_url: str, owner: Optional[Union[User, str]] = None
    ) -> ClientResult[SPSiteCreationResponse]:
        """When executing this method server MUST create a SharePoint site according to the parameters passed in the
        SPSiteCreationRequest and return the information about the site it created in the format of a
        SPSiteCreationResponse.

        Args:
            title (str): Site title
            site_url (str): Site url
            owner (str or office365.sharepoint.principal.user.User): Site owner object or principal name
        """
        return_type = ClientResult(self.context, SPSiteCreationResponse())

        def _create(owner_string: Optional[str] = None):
            request = SPSiteCreationRequest(title, site_url, owner_string)
            payload = {"request": request}
            qry = ServiceOperationQuery(self, "Create", None, payload, None, return_type)
            self.context.add_query(qry)

        from office365.sharepoint.principal.users.user import User

        if isinstance(owner, User):
            owner.ensure_property("UserPrincipalName").after_execute(lambda _: _create(owner.user_principal_name))
        else:
            _create(owner)
        return return_type

    def delete(self, site_id: str) -> Self:
        """When executing this method server MUST put the SharePoint site into recycle bin according to
        the parameter passed in the siteId, if the SharePoint site of giving siteId exists and the site has
        no attached AD group.

        Args:
            site_id (str): The GUID to uniquely identify a SharePoint site.
        """
        payload = {"siteId": site_id}
        qry = ServiceOperationQuery(self, "Delete", None, payload)
        self.context.add_query(qry)
        return self

    def get_status(self, site_url: str) -> ClientResult[SPSiteCreationResponse]:
        """When executing this method server SHOULD return a SharePoint site status in the format
        of a SPSiteCreationResponse according to the parameter passed in the url.

        Args:
            site_url (str): URL of the site to return status for
        """
        response = ClientResult(self.context, SPSiteCreationResponse())
        qry = ServiceOperationQuery(self, "Status", None, {"url": site_url}, None, response)

        def _construct_request(request: RequestOptions) -> None:
            request.method = HttpMethod.Get
            request.url += f"?url='{site_url}'"

        self.context.add_query(qry).before_execute(_construct_request)
        return response

    def get_site_url(self, site_id: str) -> ClientResult[str]:
        """Args:
        site_id (str): The GUID to uniquely identify a SharePoint site.
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "SiteUrl", None, {"siteId": site_id}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_team_channel_site_owner(self, site_id: str) -> ClientResult[GetTeamChannelSiteOwnerResponse]:
        """Args:
        site_id (str): The GUID to uniquely identify a SharePoint site.
        """
        return_type = ClientResult(self.context, GetTeamChannelSiteOwnerResponse())
        qry = ServiceOperationQuery(self, "GetTeamChannelSiteOwner", None, {"siteId": site_id}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def viva_backend_site_url_from_name(self, site_name: str) -> ClientResult[VivaSiteRequestInfo]:
        """Args:
        site_name (str):
        """
        return_type = ClientResult(self.context, VivaSiteRequestInfo())
        payload = {"siteName": site_name}
        qry = ServiceOperationQuery(self, "VivaBackendSiteUrlFromName", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Portal.SPSiteManager"

    def archive_team_channel_site(self, site_id: UUID, archive: bool) -> Self:
        """ArchiveTeamChannelSite operation.

        Args:
            site_id (UUID): siteId parameter
            archive (bool): archive parameter
        """
        qry = ServiceOperationQuery(
            self, "ArchiveTeamChannelSite", None, {"siteId": site_id, "archive": archive}, None, None
        )
        self.context.add_query(qry)
        return self

    def archive_team_connected_site(
        self,
        site_id: UUID,
        is_archive: bool,
        modern_group_member_move: GroupMoveOperation,
        all_tenant_user_move: GroupMoveOperation,
    ) -> Self:
        """ArchiveTeamConnectedSite operation.

        Args:
            site_id (UUID): SiteId parameter
            is_archive (bool): IsArchive parameter
            modern_group_member_move (GroupMoveOperation): ModernGroupMemberMove parameter
            all_tenant_user_move (GroupMoveOperation): AllTenantUserMove parameter
        """
        qry = ServiceOperationQuery(
            self,
            "ArchiveTeamConnectedSite",
            None,
            {
                "SiteId": site_id,
                "IsArchive": is_archive,
                "ModernGroupMemberMove": modern_group_member_move,
                "AllTenantUserMove": all_tenant_user_move,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def are_segments_compatible(self, segments: list[UUID]) -> ClientResult[bool]:
        """AreSegmentsCompatible operation.

        Args:
            segments (list[UUID]): segments parameter
        """
        return_type = ClientResult(self.context, bool())
        qry = FunctionQuery(self, "AreSegmentsCompatible", [GuidCollection(segments)], return_type)
        self.context.add_query(qry)
        return return_type

    def can_create_hub_joined_site(self, hub_site_id: UUID) -> ClientResult[bool]:
        """CanCreateHubJoinedSite operation.

        Args:
            hub_site_id (UUID): hubSiteId parameter
        """
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(self, "CanCreateHubJoinedSite", None, {"hubSiteId": hub_site_id}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_compatible_segments(self, segments: list[UUID]) -> ClientResult[ClientValueCollection[IBSegmentInfo]]:
        """GetCompatibleSegments operation.

        Args:
            segments (list[UUID]): segments parameter
        """
        return_type = ClientResult(self.context, ClientValueCollection[IBSegmentInfo]())
        qry = FunctionQuery(self, "GetCompatibleSegments", [GuidCollection(segments)], return_type)
        self.context.add_query(qry)
        return return_type

    def get_ib_segment_labels(self, ib_segments: list[UUID]) -> ClientResult[ClientValueCollection[IBSegmentInfo]]:
        """GetIBSegmentLabels operation.

        Args:
            ib_segments (list[UUID]): IBSegments parameter
        """
        return_type = ClientResult(self.context, ClientValueCollection[IBSegmentInfo]())
        qry = FunctionQuery(self, "GetIBSegmentLabels", [GuidCollection(ib_segments)], return_type)
        self.context.add_query(qry)
        return return_type

    def landing_site_url_from_name(self, site_name: str) -> ClientResult[VivaSiteRequestInfo]:
        """LandingSiteUrlFromName operation.

        Args:
            site_name (str): siteName parameter
        """
        return_type = ClientResult(self.context, VivaSiteRequestInfo())
        qry = FunctionQuery(self, "LandingSiteUrlFromName", [site_name], return_type)
        self.context.add_query(qry)
        return return_type

    def restore_teams_channel_site(self, site_id: UUID, related_group_id: UUID) -> Self:
        """RestoreTeamsChannelSite operation.

        Args:
            site_id (UUID): siteId parameter
            related_group_id (UUID): relatedGroupId parameter
        """
        qry = ServiceOperationQuery(
            self, "RestoreTeamsChannelSite", None, {"siteId": site_id, "relatedGroupId": related_group_id}, None, None
        )
        self.context.add_query(qry)
        return self

    def set_ib_segments(self, ib_segments: list[UUID]) -> Self:
        """SetIBSegments operation.

        Args:
            ib_segments (list[UUID]): IBSegments parameter
        """
        qry = ServiceOperationQuery(self, "SetIBSegments", None, {"IBSegments": GuidCollection(ib_segments)}, None, None)
        self.context.add_query(qry)
        return self

    def set_team_channel_site_owner(
        self, site_id: UUID, logon_name: str, secondary_logon_name: str, object_id: str, tenant_id: str
    ) -> Self:
        """SetTeamChannelSiteOwner operation.

        Args:
            site_id (UUID): siteId parameter
            logon_name (str): logonName parameter
            secondary_logon_name (str): secondaryLogonName parameter
            object_id (str): objectId parameter
            tenant_id (str): tenantId parameter
        """
        qry = ServiceOperationQuery(
            self,
            "SetTeamChannelSiteOwner",
            None,
            {
                "siteId": site_id,
                "logonName": logon_name,
                "secondaryLogonName": secondary_logon_name,
                "objectId": object_id,
                "tenantId": tenant_id,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def site_url(self, site_id: UUID) -> ClientResult[str]:
        """SiteUrl operation.

        Args:
            site_id (UUID): siteId parameter
        """
        return_type = ClientResult(self.context, str())
        qry = FunctionQuery(self, "SiteUrl", [site_id], return_type)
        self.context.add_query(qry)
        return return_type

    def status(self, url: str) -> ClientResult[SPSiteCreationResponse]:
        """Status operation.

        Args:
            url (str): url parameter
        """
        return_type = ClientResult(self.context, SPSiteCreationResponse())
        qry = FunctionQuery(self, "Status", [url], return_type)
        self.context.add_query(qry)
        return return_type

    def update_workflow2013_endpoint(self, workflow_service_address: str, workflow_hostname: str) -> Self:
        """UpdateWorkflow2013Endpoint operation.

        Args:
            workflow_service_address (str): workflowServiceAddress parameter
            workflow_hostname (str): workflowHostname parameter
        """
        qry = ServiceOperationQuery(
            self,
            "UpdateWorkflow2013Endpoint",
            None,
            {"workflowServiceAddress": workflow_service_address, "workflowHostname": workflow_hostname},
            None,
            None,
        )
        self.context.add_query(qry)
        return self
