from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class PeopleCollection(Entity):
    @staticmethod
    @site_access(SiteLevel.READ)
    def get_collaborators(context: ClientContext, top: int) -> ClientResult[str]:
        """GetCollaborators operation.

        Args:
            top (int):
                top parameter
        """
        from office365.sharepoint.userprofiles.peoplecollection import PeopleCollection

        return_type = ClientResult(context, str())
        qry = FunctionQuery(PeopleCollection(context), "GetCollaborators", [top], return_type)
        context.add_query(qry)
        return return_type

    @staticmethod
    @site_access(SiteLevel.READ)
    def get_collaborators_as_stream(context: ClientContext, top: int) -> ClientResult[bytes]:
        """GetCollaboratorsAsStream operation.

        Args:
            top (int):
                top parameter
        """
        from office365.sharepoint.userprofiles.peoplecollection import PeopleCollection

        return_type = ClientResult(context, bytes())
        qry = FunctionQuery(
            PeopleCollection(context), "GetCollaboratorsAsStream", [top], return_type, return_raw_content=True
        )
        context.add_query(qry)
        return return_type
