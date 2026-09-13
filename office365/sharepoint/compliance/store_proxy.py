from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.function import FunctionQuery
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
        context: ClientContext, site_id: str, return_type: Optional[ClientResult[bool]] = None
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
            SPPolicyStoreProxy(context), "CheckSiteIsDeletableById", None, payload, None, return_type, True
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def is_site_deletable(
        context: ClientContext, site_url: str, return_type: Optional[ClientResult[bool]] = None
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
            SPPolicyStoreProxy(context), "IsSiteDeletable", None, payload, None, return_type, True
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_available_tags_for_site(
        context: ClientContext,
        site_url: str,
        return_type: Optional[ClientResult[ClientValueCollection[ComplianceTag]]] = None,
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
            SPPolicyStoreProxy(context), "GetAvailableTagsForSite", None, payload, None, return_type, True
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
        context: ClientContext, list_url: str, return_type: Optional[ClientResult[ComplianceTag]] = None
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
            SPPolicyStoreProxy(context), "GetListComplianceTag", None, payload, None, return_type, True
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def register_site_hold_event_receiver(
        context: ClientContext, site_url: Optional[str] = None, site_id: Optional[str] = None
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
        qry = ServiceOperationQuery(binding_type, "RegisterSiteHoldEventReceiver", None, payload, None, None, True)
        context.add_query(qry)
        return binding_type

    @staticmethod
    def set_list_compliance_tag(
        context: ClientContext,
        list_url: str,
        compliance_tag_value: str,
        block_delete: Optional[bool] = None,
        block_edit: Optional[bool] = None,
        sync_to_items: Optional[bool] = None,
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
        qry = ServiceOperationQuery(binding_type, "SetListComplianceTag", None, payload, None, None, True)
        context.add_query(qry)
        return binding_type

    @staticmethod
    def lock_record_item(
        context: ClientContext,
        list_url: str,
        item_id: int,
        refresh_labeled_time: Optional[bool] = None,
        return_type: Optional[ClientResult[int]] = None,
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
        payload = {"listUrl": list_url, "itemId": item_id, "refreshLabeledTime": refresh_labeled_time}
        qry = ServiceOperationQuery(
            SPPolicyStoreProxy(context), "LockRecordItem", None, payload, None, return_type, True
        )
        context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "SP.CompliancePolicy.SPPolicyStoreProxy"

    @property
    def policy_store_url(self) -> Optional[str]:
        """Gets the PolicyStoreUrl property"""
        return self.properties.get("PolicyStoreUrl", None)

    @property
    def review_center_url(self) -> Optional[str]:
        """Gets the ReviewCenterUrl property"""
        return self.properties.get("ReviewCenterUrl", None)

    @property
    def support_content_type_retention(self) -> Optional[bool]:
        """Gets the SupportContentTypeRetention property"""
        return self.properties.get("SupportContentTypeRetention", None)

    def bulk_update_dynamic_scope_bindings(
        self, scopes_to_add: StringCollection, scopes_to_remove: StringCollection, site_id: str
    ) -> Self:
        """BulkUpdateDynamicScopeBindings operation.

        Args:
            scopes_to_add (StringCollection): scopesToAdd parameter
            scopes_to_remove (StringCollection): scopesToRemove parameter
            site_id (str): siteId parameter
        """
        qry = ServiceOperationQuery(
            self,
            "BulkUpdateDynamicScopeBindings",
            None,
            {"scopesToAdd": scopes_to_add, "scopesToRemove": scopes_to_remove, "siteId": site_id},
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def extend_review_items_retention(
        self, item_ids: ClientValueCollection, extension_date: datetime
    ) -> ClientResult[ClientValueCollection[int]]:
        """ExtendReviewItemsRetention operation.

        Args:
            item_ids (ClientValueCollection): itemIds parameter
            extension_date (datetime): extensionDate parameter
        """
        return_type = ClientResult(self.context, ClientValueCollection(int))
        qry = ServiceOperationQuery(
            self,
            "ExtendReviewItemsRetention",
            None,
            {"itemIds": item_ids, "extensionDate": extension_date},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def get_site_adaptive_policies(self, site_id: str) -> ClientResult[StringCollection]:
        """GetSiteAdaptivePolicies operation.

        Args:
            site_id (str): siteId parameter
        """
        return_type = ClientResult(self.context, StringCollection())
        qry = FunctionQuery(self, "GetSiteAdaptivePolicies", [site_id], return_type)
        self.context.add_query(qry)
        return return_type

    def get_site_adaptive_policies_v2(self, site_id: str) -> ClientResult[StringCollection]:
        """GetSiteAdaptivePoliciesV2 operation.

        Args:
            site_id (str): siteId parameter
        """
        return_type = ClientResult(self.context, StringCollection())
        qry = FunctionQuery(self, "GetSiteAdaptivePoliciesV2", [site_id], return_type)
        self.context.add_query(qry)
        return return_type

    def mark_review_items_for_deletion(
        self, item_ids: ClientValueCollection
    ) -> ClientResult[ClientValueCollection[int]]:
        """MarkReviewItemsForDeletion operation.

        Args:
            item_ids (ClientValueCollection): itemIds parameter
        """
        return_type = ClientResult(self.context, ClientValueCollection(int))
        qry = ServiceOperationQuery(self, "MarkReviewItemsForDeletion", None, {"itemIds": item_ids}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def open_binary_stream_for_original_item(self, item_id: int) -> ClientResult[bytes]:
        """OpenBinaryStreamForOriginalItem operation.

        Args:
            item_id (int): itemId parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self, "OpenBinaryStreamForOriginalItem", None, {"itemId": item_id}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def remove_container_retention_policy(self, site_id: str) -> Self:
        """RemoveContainerRetentionPolicy operation.

        Args:
            site_id (str): siteId parameter
        """
        qry = ServiceOperationQuery(self, "RemoveContainerRetentionPolicy", None, {"siteId": site_id}, None, None)
        self.context.add_query(qry)
        return self

    def remove_container_settings(self, external_id: StringCollection) -> Self:
        """RemoveContainerSettings operation.

        Args:
            external_id (StringCollection): externalId parameter
        """
        qry = ServiceOperationQuery(self, "RemoveContainerSettings", None, {"externalId": external_id}, None, None)
        self.context.add_query(qry)
        return self

    def retag_review_items(
        self,
        item_ids: ClientValueCollection,
        new_tag: str,
        new_tag_is_record: bool,
        new_tag_block_delete: bool,
        new_tag_is_event_based: bool,
    ) -> ClientResult[ClientValueCollection[int]]:
        """RetagReviewItems operation.

        Args:
            item_ids (ClientValueCollection): itemIds parameter
            new_tag (str): newTag parameter
            new_tag_is_record (bool): newTagIsRecord parameter
            new_tag_block_delete (bool): newTagBlockDelete parameter
            new_tag_is_event_based (bool): newTagIsEventBased parameter
        """
        return_type = ClientResult(self.context, ClientValueCollection(int))
        qry = ServiceOperationQuery(
            self,
            "RetagReviewItems",
            None,
            {
                "itemIds": item_ids,
                "newTag": new_tag,
                "newTagIsRecord": new_tag_is_record,
                "newTagBlockDelete": new_tag_block_delete,
                "newTagIsEventBased": new_tag_is_event_based,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def retag_review_items_with_metas(
        self, item_ids: ClientValueCollection, new_tag_name: str, new_tag_metas: StringCollection
    ) -> ClientResult[ClientValueCollection[int]]:
        """RetagReviewItemsWithMetas operation.

        Args:
            item_ids (ClientValueCollection): itemIds parameter
            new_tag_name (str): newTagName parameter
            new_tag_metas (StringCollection): newTagMetas parameter
        """
        return_type = ClientResult(self.context, ClientValueCollection(int))
        qry = ServiceOperationQuery(
            self,
            "RetagReviewItemsWithMetas",
            None,
            {"itemIds": item_ids, "newTagName": new_tag_name, "newTagMetas": new_tag_metas},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def retag_unified_review_items_with_metas(
        self, item_ids: StringCollection, original_tag_name: str, new_tag_name: str, new_tag_metas: StringCollection
    ) -> ClientResult[StringCollection]:
        """RetagUnifiedReviewItemsWithMetas operation.

        Args:
            item_ids (StringCollection): itemIds parameter
            original_tag_name (str): originalTagName parameter
            new_tag_name (str): newTagName parameter
            new_tag_metas (StringCollection): newTagMetas parameter
        """
        return_type = ClientResult(self.context, StringCollection())
        qry = ServiceOperationQuery(
            self,
            "RetagUnifiedReviewItemsWithMetas",
            None,
            {
                "itemIds": item_ids,
                "originalTagName": original_tag_name,
                "newTagName": new_tag_name,
                "newTagMetas": new_tag_metas,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def set_container_retention_policy(self, site_id: str, default_container_label: UUID) -> Self:
        """SetContainerRetentionPolicy operation.

        Args:
            site_id (str): siteId parameter
            default_container_label (UUID): defaultContainerLabel parameter
        """
        qry = ServiceOperationQuery(
            self,
            "SetContainerRetentionPolicy",
            None,
            {"siteId": site_id, "defaultContainerLabel": default_container_label},
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def update_container_setting(self, site_id: str, external_id: str, setting_type: int, setting: str) -> Self:
        """UpdateContainerSetting operation.

        Args:
            site_id (str): siteId parameter
            external_id (str): externalId parameter
            setting_type (int): settingType parameter
            setting (str): setting parameter
        """
        qry = ServiceOperationQuery(
            self,
            "UpdateContainerSetting",
            None,
            {"siteId": site_id, "externalId": external_id, "settingType": setting_type, "setting": setting},
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def update_site_adaptive_policies(
        self, policies_to_add: StringCollection, policies_to_remove: StringCollection, site_id: str
    ) -> Self:
        """UpdateSiteAdaptivePolicies operation.

        Args:
            policies_to_add (StringCollection): policiesToAdd parameter
            policies_to_remove (StringCollection): policiesToRemove parameter
            site_id (str): siteId parameter
        """
        qry = ServiceOperationQuery(
            self,
            "UpdateSiteAdaptivePolicies",
            None,
            {"policiesToAdd": policies_to_add, "policiesToRemove": policies_to_remove, "siteId": site_id},
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def update_site_adaptive_policies_v2(
        self, policies_to_add: StringCollection, policies_to_remove: StringCollection, site_id: str
    ) -> Self:
        """UpdateSiteAdaptivePoliciesV2 operation.

        Args:
            policies_to_add (StringCollection): policiesToAdd parameter
            policies_to_remove (StringCollection): policiesToRemove parameter
            site_id (str): siteId parameter
        """
        qry = ServiceOperationQuery(
            self,
            "UpdateSiteAdaptivePoliciesV2",
            None,
            {"policiesToAdd": policies_to_add, "policiesToRemove": policies_to_remove, "siteId": site_id},
            None,
            None,
        )
        self.context.add_query(qry)
        return self
