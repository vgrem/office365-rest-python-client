from __future__ import annotations

from typing import Optional

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity
from office365.sharepoint.sites.manager.baaa_request import BAAARequest
from office365.sharepoint.sites.manager.baaa_response import BAAAResponse
from office365.sharepoint.sites.manager.documents_data_source import DocumentsDataSource
from office365.sharepoint.sites.manager.inactive_documents_query_result import InactiveDocumentsQueryResult
from office365.sharepoint.sites.manager.missinglinksresult import MissingLinksResult
from office365.sharepoint.sites.manager.retirablepagesqueryresult import RetirablePagesQueryResult
from office365.sharepoint.sites.manager.sitemanagersignals import SiteManagerSignals
from office365.sharepoint.sites.manager.suggestionitem import SuggestionItem
from office365.sharepoint.sites.manager.topsitefilesresult import TopSiteFilesResult


class SiteManagerService(Entity):
    """ """

    @property
    def resource_path(self):
        if self._resource_path is None:
            self._resource_path = StaticPath("Microsoft.SharePoint.SiteManager.SiteManagerService")
        return self._resource_path

    def top_files(self, max_count: Optional[int] = None) -> ClientResult[TopSiteFilesResult]:
        """ """
        return_type = ClientResult(self.context, TopSiteFilesResult())
        payload = {"maxCount": max_count}
        qry = ServiceOperationQuery(self, "TopFiles", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.SiteManagerService"

    def add_suggestion_items(self, suggestion_items: ClientValueCollection[SuggestionItem]) -> Self:
        """AddSuggestionItems operation.

        Args:
            suggestion_items (ClientValueCollection[SuggestionItem]): suggestionItems parameter
        """
        qry = ServiceOperationQuery(self, "AddSuggestionItems", None, {"suggestionItems": suggestion_items}, None, None)
        self.context.add_query(qry)
        return self

    def delete_suggestion_items_by_identifiers(self, card_type: int, identifiers: list[str]) -> Self:
        """DeleteSuggestionItemsByIdentifiers operation.

        Args:
            card_type (int): cardType parameter
            identifiers (list[str]): identifiers parameter
        """
        qry = ServiceOperationQuery(
            self,
            "DeleteSuggestionItemsByIdentifiers",
            None,
            {"cardType": card_type, "identifiers": StringCollection(identifiers)},
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def ensure_missing_links_list_early_activate_feature(self) -> Self:
        """EnsureMissingLinksListEarlyActivateFeature operation."""
        qry = ServiceOperationQuery(self, "EnsureMissingLinksListEarlyActivateFeature", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def ensure_missing_links_list_feature(self) -> Self:
        """EnsureMissingLinksListFeature operation."""
        qry = ServiceOperationQuery(self, "EnsureMissingLinksListFeature", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def ensure_redirect_url_list_feature(self) -> Self:
        """EnsureRedirectUrlListFeature operation."""
        qry = ServiceOperationQuery(self, "EnsureRedirectUrlListFeature", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def ensure_retire_page_feature(self) -> Self:
        """EnsureRetirePageFeature operation."""
        qry = ServiceOperationQuery(self, "EnsureRetirePageFeature", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def ensure_suggestion_list_feature(self) -> Self:
        """EnsureSuggestionListFeature operation."""
        qry = ServiceOperationQuery(self, "EnsureSuggestionListFeature", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def get_dismissed_content_gap_suggestions(self) -> ClientResult[ClientValueCollection[SuggestionItem]]:
        """GetDismissedContentGapSuggestions operation."""
        return_type = ClientResult(self.context, ClientValueCollection[SuggestionItem]())
        qry = FunctionQuery(self, "GetDismissedContentGapSuggestions", [], return_type)
        self.context.add_query(qry)
        return return_type

    def inactive_documents(
        self, top: int, skip_token: str, last_access_days: int, data_sources: ClientValueCollection[DocumentsDataSource]
    ) -> ClientResult[InactiveDocumentsQueryResult]:
        """InactiveDocuments operation.

        Args:
            top (int): top parameter
            skip_token (str): skipToken parameter
            last_access_days (int): lastAccessDays parameter
            data_sources (ClientValueCollection[DocumentsDataSource]): dataSources parameter
        """
        return_type = ClientResult(self.context, InactiveDocumentsQueryResult())
        qry = FunctionQuery(self, "InactiveDocuments", [top, skip_token, last_access_days, data_sources], return_type)
        self.context.add_query(qry)
        return return_type

    def log_missing_link(self, referrer_url: str, destination_url: str) -> Self:
        """LogMissingLink operation.

        Args:
            referrer_url (str): referrerUrl parameter
            destination_url (str): destinationUrl parameter
        """
        qry = ServiceOperationQuery(
            self, "LogMissingLink", None, {"referrerUrl": referrer_url, "destinationUrl": destination_url}, None, None
        )
        self.context.add_query(qry)
        return self

    def perform_baaa(self, baaa_request: BAAARequest) -> ClientResult[BAAAResponse]:
        """PerformBAAA operation.

        Args:
            baaa_request (BAAARequest): baaaRequest parameter
        """
        return_type = ClientResult(self.context, BAAAResponse())
        qry = ServiceOperationQuery(self, "PerformBAAA", None, {"baaaRequest": baaa_request}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def remove_missing_links_list_early_activate_feature(self) -> Self:
        """RemoveMissingLinksListEarlyActivateFeature operation."""
        qry = ServiceOperationQuery(self, "RemoveMissingLinksListEarlyActivateFeature", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def retirable_pages(
        self,
        top: int,
        skip_token: str,
        is_debug: bool,
        snoozed_paths: str,
        is_document: bool,
        data_sources: ClientValueCollection[DocumentsDataSource],
        use_spo: bool,
        last_accessed_days: int,
    ) -> ClientResult[RetirablePagesQueryResult]:
        """RetirablePages operation.

        Args:
            top (int): top parameter
            skip_token (str): skipToken parameter
            is_debug (bool): isDebug parameter
            snoozed_paths (str): snoozedPaths parameter
            is_document (bool): isDocument parameter
            data_sources (ClientValueCollection[DocumentsDataSource]): dataSources parameter
            use_spo (bool): useSPO parameter
            last_accessed_days (int): lastAccessedDays parameter
        """
        return_type = ClientResult(self.context, RetirablePagesQueryResult())
        qry = FunctionQuery(
            self,
            "RetirablePages",
            [top, skip_token, is_debug, snoozed_paths, is_document, data_sources, use_spo, last_accessed_days],
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def retired_pages_view(self) -> Self:
        """RetiredPagesView operation."""
        qry = FunctionQuery(self, "RetiredPagesView", [], None)
        self.context.add_query(qry)
        return self

    def set_site_manager_signals(self, signals: SiteManagerSignals) -> Self:
        """SetSiteManagerSignals operation.

        Args:
            signals (SiteManagerSignals): signals parameter
        """
        qry = ServiceOperationQuery(self, "SetSiteManagerSignals", None, {"signals": signals}, None, None)
        self.context.add_query(qry)
        return self

    def site_manager_signals(self) -> ClientResult[SiteManagerSignals]:
        """SiteManagerSignals operation."""
        return_type = ClientResult(self.context, SiteManagerSignals())
        qry = FunctionQuery(self, "SiteManagerSignals", [], return_type)
        self.context.add_query(qry)
        return return_type

    def top_missing_links(self, max_count: int, snoozed_links: str) -> ClientResult[MissingLinksResult]:
        """TopMissingLinks operation.

        Args:
            max_count (int): maxCount parameter
            snoozed_links (str): snoozedLinks parameter
        """
        return_type = ClientResult(self.context, MissingLinksResult())
        qry = FunctionQuery(self, "TopMissingLinks", [max_count, snoozed_links], return_type)
        self.context.add_query(qry)
        return return_type
