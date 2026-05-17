from typing import Optional

from office365.runtime.client_value import ClientValue


class InDocFacet(ClientValue):
    """"""

    def __init__(
        self,
        contentId=None,
        navigationId=None,
        content_id: Optional[str] = None,
        navigation_id: Optional[str] = None,
    ):
        self.contentId = contentId
        self.navigationId = navigationId
        self.contentId = content_id
        self.navigationId = navigation_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.InDocFacet"
