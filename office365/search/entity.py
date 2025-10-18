from typing import List, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.v4.entity import EntityPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.search.acronyms.acronym import Acronym
from office365.search.bookmarks.bookmark import Bookmark
from office365.search.entity_type import EntityType
from office365.search.hits.hit import SearchHit
from office365.search.qnas.qna import Qna
from office365.search.query import SearchQuery
from office365.search.request import SearchRequest
from office365.search.response import SearchResponse


class SearchEntity(Entity):
    """
    A top level object representing the Microsoft Search API endpoint. It does not behave as any other resource
    in Graph, but serves as an anchor to the query action.
    """

    def query(
        self,
        query_string: str,
        entity_types: Optional[List[str]] = None,
        page_from: Optional[int] = None,
        size: Optional[int] = None,
        enable_top_results: Optional[bool] = None,
        region: Optional[str] = None,
    ) -> ClientResult[ClientValueCollection[SearchResponse]]:
        """
        Runs the query specified in the request body. Search results are provided in the response.

        :param str query_string: Contains the query terms.
        :param list[str] entity_types: One or more types of resources expected in the response.
            Possible values are: list, site, listItem, message, event, drive, driveItem, externalItem.
        :param int page_from: Specifies the offset for the search results. Offset 0 returns the very first result.
        :param int size: The size of the page to be retrieved. The maximum value is 500. Optional.
        :param bool enable_top_results: This triggers hybrid sort for messages
        :param str region: The geographic location for the search. Required for searches that use application
             permissions. For details, see Get the region value.
        """
        search_request = SearchRequest(
            query=SearchQuery(query_string),
            entity_types=entity_types,
            page_from=page_from,
            size=size,
            enable_top_results=enable_top_results,
            region=region,
        )

        def _patch_hit(search_hit: SearchHit) -> None:
            resource_type_name = search_hit.get_property("resource").get("@odata.type", None)
            resource_type = EntityType.resolve(resource_type_name)
            resource = resource_type(self.context, EntityPath())
            self.context.pending_request().map_json(search_hit.resource, resource)
            search_hit.set_property("resource", resource)

        def _process_response(
            result: ClientResult[ClientValueCollection[SearchResponse]],
        ) -> None:
            for item in result.value:
                for hcs in item.hitsContainers:
                    [_patch_hit(hit) for hit in hcs.hits]

        payload = {"requests": ClientValueCollection(SearchRequest, [search_request])}
        return_type = ClientResult(self.context, ClientValueCollection(SearchResponse))
        qry = ServiceOperationQuery(self, "query", None, payload, None, return_type)
        self.context.add_query(qry).after_query_execute(_process_response)
        return return_type

    def query_messages(
        self,
        query_string: str,
        page_from: int = None,
        size: int = None,
        enable_top_results: bool = None,
    ) -> ClientResult[ClientValueCollection[SearchResponse]]:
        """Searches Outlook messages. Alias to query method
        :param str query_string: Contains the query terms.
        :param int page_from: Specifies the offset for the search results. Offset 0 returns the very first result.
        :param int size: The size of the page to be retrieved. The maximum value is 500. Optional.
        :param bool enable_top_results: This triggers hybrid sort for messages
        """
        return self.query(
            query_string,
            entity_types=[EntityType.message],
            page_from=page_from,
            size=size,
            enable_top_results=enable_top_results,
        )

    def query_events(self, query_string: str) -> ClientResult[ClientValueCollection[SearchResponse]]:
        """Searches Outlook calendar events. Alias to query method
        :param str query_string: Contains the query terms.
        """
        return self.query(query_string, entity_types=[EntityType.event])

    def query_drive_items(
        self, query_string: str, page_from: int = None, size: int = None
    ) -> ClientResult[ClientValueCollection[SearchResponse]]:
        """Searches OneDrive items. Alias to query method
        :param str query_string: Contains the query terms.
        :param int page_from: Specifies the offset for the search results. Offset 0 returns the very first result.
        :param int size: The size of the page to be retrieved. The maximum value is 500.
        """
        return self.query(
            query_string,
            entity_types=[EntityType.driveItem],
            page_from=page_from,
            size=size,
        )

    def query_list_items(
        self,
        query_string: str,
        page_from: int = None,
        size: int = None,
        region: str = None,
    ) -> ClientResult[ClientValueCollection[SearchResponse]]:
        """Searches list items. Alias to query method

        :param str query_string: Contains the query terms.
        :param int page_from: Specifies the offset for the search results. Offset 0 returns the very first result.
        :param int size: The size of the page to be retrieved. The maximum value is 500.
        :param str region: The geographic location for the search. Required for searches that use application
        """
        return self.query(
            query_string,
            entity_types=[EntityType.listItem],
            page_from=page_from,
            size=size,
            region=region,
        )

    def query_peoples(
        self,
        query_string: str,
        page_from: int = None,
        size: int = None,
        region: str = None,
    ) -> ClientResult[ClientValueCollection[SearchResponse]]:
        """Searches peoples. Alias to query method

        :param str query_string: Contains the query terms.
        :param int page_from: Specifies the offset for the search results. Offset 0 returns the very first result.
        :param int size: The size of the page to be retrieved. The maximum value is 500.
        :param str region: The geographic location for the search. Required for searches that use application
        """
        return self.query(
            query_string,
            entity_types=[EntityType.person],
            page_from=page_from,
            size=size,
            region=region,
        )

    def query_sites(
        self,
        query_string: str,
        page_from: int = None,
        size: int = None,
        region: str = None,
    ) -> ClientResult[ClientValueCollection[SearchResponse]]:
        """Searches sites. Alias to query method

        :param str query_string: Contains the query terms.
        :param int page_from: Specifies the offset for the search results. Offset 0 returns the very first result.
        :param int size: The size of the page to be retrieved. The maximum value is 500.
        :param str region: The geographic location for the search. Required for searches that use application
        """
        return self.query(
            query_string,
            entity_types=[EntityType.site],
            page_from=page_from,
            size=size,
            region=region,
        )

    def query_chat_messages(
        self,
        query_string: str,
        page_from: int = None,
        size: int = None,
        region: str = None,
    ) -> ClientResult[ClientValueCollection[SearchResponse]]:
        """Searches Teams chat messages. Alias to query method

        :param str query_string: Contains the query terms.
        :param int page_from: Specifies the offset for the search results. Offset 0 returns the very first result.
        :param int size: The size of the page to be retrieved. The maximum value is 500.
        :param str region: The geographic location for the search. Required for searches that use application
        """
        return self.query(
            query_string,
            entity_types=[EntityType.chatMessage],
            page_from=page_from,
            size=size,
            region=region,
        )

    @property
    def acronyms(self) -> EntityCollection[Acronym]:
        """Administrative answer in Microsoft Search results to define common acronyms in an organization."""
        return self.properties.get(
            "acronyms",
            EntityCollection(
                self.context,
                Acronym,
                ResourcePath("acronyms", self.resource_path),
            ),
        )

    @property
    def bookmarks(self) -> EntityCollection[Bookmark]:
        """Administrative answer in Microsoft Search results for common search queries in an organization."""
        return self.properties.get(
            "bookmarks",
            EntityCollection(
                self.context,
                Bookmark,
                ResourcePath("bookmarks", self.resource_path),
            ),
        )

    @property
    def qnas(self) -> EntityCollection[Qna]:
        """Administrative answer in Microsoft Search results that provide answers for specific search keywords in
        an organization."""
        return self.properties.get(
            "qnas",
            EntityCollection(
                self.context,
                Qna,
                ResourcePath("qnas", self.resource_path),
            ),
        )
