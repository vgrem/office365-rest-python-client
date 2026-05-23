from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.sitedesigns.creation_info import SiteDesignCreationInfo
from office365.sharepoint.sitedesigns.metadata import SiteDesignMetadata
from office365.sharepoint.sitedesigns.principal import SiteDesignPrincipal
from office365.sharepoint.sitedesigns.task import SiteDesignTask
from office365.sharepoint.sitescripts.action_result import SiteScriptActionResult
from office365.sharepoint.sitescripts.metadata import SiteScriptMetadata
from office365.sharepoint.sitescripts.serialization_info import SiteScriptSerializationInfo
from office365.sharepoint.sitescripts.serialization_result import SiteScriptSerializationResult

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class SiteScriptUtility(Entity):
    """Automate provisioning new or existing modern SharePoint sites with custom configurations."""

    def __init__(self, context: ClientContext) -> None:
        path = StaticPath("Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteScriptUtility")
        super().__init__(context, path)

    @staticmethod
    def create_list_design(context: ClientContext, info: SiteDesignCreationInfo) -> ClientResult[SiteDesignMetadata]:
        """Creates a list design available when users create a list from the SharePoint start page.

        Args:
            context: SharePoint client context
            info: Site design creation parameters
        """
        return_type = ClientResult(context, SiteDesignMetadata())
        utility = SiteScriptUtility(context)
        payload = {"info": info}
        qry = ServiceOperationQuery(utility, "CreateListDesign", None, payload, None, return_type, True)
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_list_designs(context: ClientContext, store: str | None = None) -> ClientResult[SiteDesignMetadata]:
        """Gets list designs.

        Args:
            context: SharePoint client context
            store: Optional store identifier
        """
        return_type = ClientResult(context, SiteDesignMetadata())
        utility = SiteScriptUtility(context)
        payload = {"store": store}
        qry = ServiceOperationQuery(utility, "GetListDesigns", None, payload, None, return_type, True)
        context.add_query(qry)
        return return_type

    @staticmethod
    def add_site_design_task(context: ClientContext, web_url: str, site_design_id: str) -> ClientResult[SiteDesignTask]:
        """Schedules a site design for asynchronous application to a site.

        Args:
            context: SharePoint client context
            web_url: URL of the target web
            site_design_id: ID of the site design to apply
        """
        return_type = ClientResult(context, SiteDesignTask())
        utility = SiteScriptUtility(context)
        payload = {"webUrl": web_url, "siteDesignId": site_design_id}
        qry = ServiceOperationQuery(utility, "AddSiteDesignTask", None, payload, None, return_type, True)
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_site_script_from_list(
        context: ClientContext,
        list_url: str,
        options: Dict[str, Any] | None = None,
        return_type: ClientResult[str] | None = None,
    ) -> ClientResult[str]:
        """Creates site script JSON from an existing SharePoint list.

        Args:
            context: SharePoint client context
            list_url: URL of the list
            options: Serialization options
            return_type: Optional pre-built return type
        """
        if return_type is None:
            return_type = ClientResult(context)
        payload = {"listUrl": list_url, "options": options}
        utility = SiteScriptUtility(context)
        qry = ServiceOperationQuery(utility, "GetSiteScriptFromList", None, payload, None, return_type, True)
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_site_script_from_web(
        context: ClientContext,
        web_url: str,
        info: SiteScriptSerializationInfo | None = None,
        return_type: ClientResult[SiteScriptSerializationResult] | None = None,
    ) -> ClientResult[SiteScriptSerializationResult]:
        """Creates site script JSON from an existing SharePoint site.

        Args:
            context: SharePoint client context
            web_url: URL of the web
            info: Serialization options
            return_type: Optional pre-built return type
        """
        if return_type is None:
            return_type = ClientResult(context, SiteScriptSerializationResult())
        payload = {"webUrl": web_url, "info": info}
        utility = SiteScriptUtility(context)
        qry = ServiceOperationQuery(utility, "GetSiteScriptFromWeb", None, payload, None, return_type, True)
        context.add_query(qry)
        return return_type

    @staticmethod
    def create_site_script(
        context: ClientContext, title: str, description: str, content: dict[str, Any]
    ) -> ClientResult[SiteScriptMetadata]:
        """Creates a new site script.

        Args:
            context: SharePoint client context
            title: Display name for the script
            description: Description of what the script does
            content: JSON dict of site script actions
        """
        return_type = ClientResult(context, SiteScriptMetadata())
        utility = SiteScriptUtility(context)
        params = {
            "Title": title,
            "Description": description,
        }
        qry = ServiceOperationQuery(utility, "CreateSiteScript", params, content, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def delete_site_script(context: ClientContext, id_: str) -> SiteScriptUtility:
        """Deletes a site script.

        Args:
            context: SharePoint client context
            id_: ID of the site script to delete
        """
        utility = SiteScriptUtility(context)
        payload = {"id": id_}
        qry = ServiceOperationQuery(utility, "DeleteSiteScript", None, payload, None, None)
        qry.static = True
        context.add_query(qry)
        return utility

    @staticmethod
    def get_site_scripts(
        context: ClientContext, store: str | None = None
    ) -> ClientResult[ClientValueCollection[SiteScriptMetadata]]:
        """Gets all existing site scripts.

        Args:
            context: SharePoint client context
            store: Optional store identifier
        """
        return_type = ClientResult(context, ClientValueCollection(SiteScriptMetadata))
        utility = SiteScriptUtility(context)
        payload = {"store": store}
        qry = ServiceOperationQuery(utility, "GetSiteScripts", None, payload, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def execute_site_script_action(
        context: ClientContext, action_definition: str
    ) -> ClientResult[ClientValueCollection[SiteScriptActionResult]]:
        """Executes a single site script action.

        Args:
            context: SharePoint client context
            action_definition: JSON string of the action to execute
        """
        return_type = ClientResult(context, ClientValueCollection(SiteScriptActionResult))
        utility = SiteScriptUtility(context)
        payload = {"actionDefinition": action_definition}
        qry = ServiceOperationQuery(utility, "ExecuteSiteScriptAction", None, payload, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def create_site_design(context: ClientContext, info: SiteDesignCreationInfo) -> ClientResult[SiteDesignMetadata]:
        """Creates a site design available when users create a new site from the SharePoint start page.

        Args:
            context: SharePoint client context
            info: Site design creation parameters
        """
        return_type = ClientResult(context, SiteDesignMetadata())
        utility = SiteScriptUtility(context)
        payload = {"info": info}
        qry = ServiceOperationQuery(utility, "CreateSiteDesign", None, payload, None, return_type, True)
        context.add_query(qry)
        return return_type

    @staticmethod
    def update_site_design(context: ClientContext, update_info: SiteDesignMetadata) -> ClientResult[SiteDesignMetadata]:
        """Updates a site design with new values.

        Args:
            context: SharePoint client context
            update_info: Site design metadata with updated fields
        """
        return_type = ClientResult(context, SiteDesignMetadata())
        utility = SiteScriptUtility(context)
        payload = {"updateInfo": update_info}
        qry = ServiceOperationQuery(utility, "UpdateSiteDesign", None, payload, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_site_designs(
        context: ClientContext, include_untargeted: bool = True, store: int | None = None
    ) -> ClientResult[ClientValueCollection[SiteDesignMetadata]]:
        """Gets all existing site designs.

        Args:
            context: SharePoint client context
            include_untargeted: Whether to include designs not targeted at the current web template
            store: Optional store identifier
        """
        return_type = ClientResult(context, ClientValueCollection(SiteDesignMetadata))
        utility = SiteScriptUtility(context)
        payload = {"includeUntargeted": include_untargeted, "store": store}
        qry = ServiceOperationQuery(utility, "GetSiteDesigns", None, payload, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_site_design_stages(context: ClientContext, site_design_id: str) -> ClientResult:
        """Gets the stages of a site design.

        Args:
            context: SharePoint client context
            site_design_id: ID of the site design
        """
        return_type = ClientResult(context)
        utility = SiteScriptUtility(context)
        qry = ServiceOperationQuery(utility, "GetSiteDesignStages", [site_design_id], None, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_site_design_metadata(
        context: ClientContext, _id: str, store: str | None = None
    ) -> ClientResult[SiteDesignMetadata]:
        """Gets metadata for a specific site design.

        Args:
            context: SharePoint client context
            _id: ID of the site design
            store: Optional store identifier
        """
        return_type = ClientResult(context, SiteDesignMetadata())
        utility = SiteScriptUtility(context)
        payload = {"id": _id, "store": store}
        qry = ServiceOperationQuery(utility, "GetSiteDesignMetadata", None, payload, None, return_type, True)
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_site_design_rights(context: ClientContext, id_: str) -> EntityCollection[SiteDesignPrincipal]:
        """Gets principals that have access to a site design.

        Args:
            context: SharePoint client context
            id_: ID of the site design
        """
        return_type = EntityCollection(context, SiteDesignPrincipal)
        utility = SiteScriptUtility(context)
        qry = ServiceOperationQuery(utility, "GetSiteDesignRights", [id_], None, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def grant_site_design_rights(
        context: ClientContext, _id: str, principal_names: list[str], granted_rights: int
    ) -> SiteScriptUtility:
        """Grants access to a site design for one or more principals.

        Args:
            context: SharePoint client context
            _id: ID of the site design
            principal_names: List of principal names (users/groups) to grant access
            granted_rights: Rights value to grant (1 = View)
        """
        utility = SiteScriptUtility(context)
        payload = {
            "id": _id,
            "principalNames": ClientValueCollection(str, principal_names),
            "grantedRights": granted_rights,
        }
        qry = ServiceOperationQuery(utility, "GrantSiteDesignRights", None, payload)
        qry.static = True
        context.add_query(qry)
        return utility

    @staticmethod
    def delete_site_design(context: ClientContext, _id: str) -> SiteScriptUtility:
        """Deletes a site design.

        Args:
            context: SharePoint client context
            _id: ID of the site design to delete
        """
        utility = SiteScriptUtility(context)
        qry = ServiceOperationQuery(utility, "DeleteSiteDesign", [_id])
        qry.static = True
        context.add_query(qry)
        return utility

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteScriptUtility"
