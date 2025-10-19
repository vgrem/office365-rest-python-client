from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.compliance.tags.tag import ComplianceTag
from office365.sharepoint.entity import Entity

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class SPPolicyStoreProxy(Entity):
    """
    Represents a proxy to the SharePoint policy store for compliance and retention operations.

    This class provides methods to manage compliance tags, retention policies,
    site deletion checks, and record management in SharePoint.
    """

    @staticmethod
    def check_site_is_deletable_by_id(
        context: ClientContext,
        site_id: str,
        return_type: Optional[ClientResult[bool]] = None,
    ) -> ClientResult[bool]:
        """
        Checks whether a site can be deleted based on its ID and compliance policies.

        Args:
            context: SharePoint client context
            site_id: The unique identifier of the site to check
            return_type: Optional client result object for the operation

        Returns:
            ClientResult[bool]: Result indicating whether the site can be deleted

        Remarks:
            This method considers compliance policies, retention holds, and other
            governance rules that might prevent site deletion.
        """
        if return_type is None:
            return_type = ClientResult(context, bool())
        payload = {"siteId": site_id}
        qry = ServiceOperationQuery(
            SPPolicyStoreProxy(context),
            "CheckSiteIsDeletableById",
            None,
            payload,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def is_site_deletable(
        context: ClientContext,
        site_url: str,
        return_type: Optional[ClientResult[bool]] = None,
    ) -> ClientResult[bool]:
        """
        Determines if a site can be deleted based on its URL and compliance policies.

        Args:
            context: SharePoint client context
            site_url: The URL of the site to check
            return_type: Optional client result object for the operation

        Returns:
            ClientResult[bool]: Result indicating whether the site can be deleted
        """
        if return_type is None:
            return_type = ClientResult(context, bool())
        payload = {"siteUrl": site_url}
        qry = ServiceOperationQuery(
            SPPolicyStoreProxy(context),
            "IsSiteDeletable",
            None,
            payload,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_available_tags_for_site(
        context: ClientContext, site_url: str, return_type: ClientResult[ClientValueCollection[ComplianceTag]] = None
    ) -> ClientResult[ClientValueCollection[ComplianceTag]]:
        """
        Retrieves all available compliance tags that can be applied to a site.

        Args:
            context: SharePoint client context
            site_url: The URL of the site to get available tags for
            return_type: Optional client result object for the operation

        Returns:
            ClientResult[ClientValueCollection[ComplianceTag]]: Collection of available compliance tags

        Remarks:
            Compliance tags are retention labels that can be applied to content
            to enforce retention policies and records management.
        """
        if return_type is None:
            return_type = ClientResult(context, ClientValueCollection(ComplianceTag))
        payload = {"siteUrl": site_url}
        qry = ServiceOperationQuery(
            SPPolicyStoreProxy(context),
            "GetAvailableTagsForSite",
            None,
            payload,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    def get_dynamic_scope_binding_by_site_id(self, site_id: str) -> ClientResult[StringCollection]:
        """
        Gets dynamic scope bindings for a specific site by its ID.

        Args:
            site_id: The unique identifier of the site

        Returns:
            ClientResult[StringCollection]: Collection of dynamic scope bindings

        Remarks:
            Dynamic scopes are used in compliance policies to dynamically determine
            which sites the policy applies to based on conditions.
        """
        return_type = ClientResult(self.context, StringCollection())
        payload = {"siteId": site_id}
        qry = ServiceOperationQuery(self, "GetDynamicScopeBindingBySiteId", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @staticmethod
    def get_list_compliance_tag(
        context: ClientContext,
        list_url: str,
        return_type: ClientResult[ComplianceTag] = None,
    ) -> ClientResult[ComplianceTag]:
        """
        Gets the compliance tag currently applied to a list or document library.

        Args:
            context: SharePoint client context
            list_url: The URL of the list or document library
            return_type: Optional client result object for the operation

        Returns:
            ClientResult[ComplianceTag]: The compliance tag applied to the list
        """
        if return_type is None:
            return_type = ClientResult(context, ComplianceTag())
        payload = {"listUrl": list_url}
        qry = ServiceOperationQuery(
            SPPolicyStoreProxy(context),
            "GetListComplianceTag",
            None,
            payload,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def register_site_hold_event_receiver(
        context: ClientContext, site_url: str = None, site_id: str = None
    ) -> SPPolicyStoreProxy:
        """
        Registers an event receiver for site hold operations.

        Args:
            context: SharePoint client context
            site_url: The URL of the site (optional if site_id is provided)
            site_id: The unique identifier of the site (optional if site_url is provided)

        Returns:
            SPPolicyStoreProxy: The policy store proxy instance

        Remarks:
            This method enables receiving events when sites are placed on hold
            for legal or compliance reasons.
        """
        payload = {"siteUrl": site_url, "siteId": site_id}
        binding_type = SPPolicyStoreProxy(context)
        qry = ServiceOperationQuery(
            binding_type,
            "RegisterSiteHoldEventReceiver",
            None,
            payload,
            None,
            None,
            True,
        )
        context.add_query(qry)
        return binding_type

    @staticmethod
    def set_list_compliance_tag(
        context: ClientContext,
        list_url: str,
        compliance_tag_value: str,
        block_delete: bool = None,
        block_edit: bool = None,
        sync_to_items: bool = None,
    ) -> SPPolicyStoreProxy:
        """Apply a retention label ("compliance tag") to a list or document library."""
        payload = {
            "listUrl": list_url,
            "complianceTagValue": compliance_tag_value,
            "blockDelete": block_delete,
            "blockEdit": block_edit,
            "syncToItems": sync_to_items,
        }
        binding_type = SPPolicyStoreProxy(context)
        qry = ServiceOperationQuery(
            binding_type,
            "SetListComplianceTag",
            None,
            payload,
            None,
            None,
            True,
        )
        context.add_query(qry)
        return binding_type

    @staticmethod
    def lock_record_item(
        context: ClientContext,
        list_url: str,
        item_id: int,
        refresh_labeled_time: bool = None,
        return_type: ClientResult[int] = None,
    ) -> ClientResult[int]:
        """
        Locks a record item to prevent modifications.

        Args:
            context: SharePoint client context
            list_url: The URL of the list containing the item
            item_id: The ID of the item to lock
            refresh_labeled_time: Whether to refresh the labeled timestamp (optional)
            return_type: Optional client result object for the operation

        Returns:
            ClientResult[int]: Result containing status or identifier of the operation

        Remarks:
            Locking a record item typically prevents any modifications to ensure
            the integrity of records for compliance and legal purposes.
        """
        if return_type is None:
            return_type = ClientResult(context, int())
        payload = {
            "listUrl": list_url,
            "itemId": item_id,
            "refreshLabeledTime": refresh_labeled_time,
        }

        qry = ServiceOperationQuery(
            SPPolicyStoreProxy(context),
            "LockRecordItem",
            None,
            payload,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "SP.CompliancePolicy.SPPolicyStoreProxy"
