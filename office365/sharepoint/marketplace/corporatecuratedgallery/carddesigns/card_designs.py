from uuid import UUID

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.marketplace.corporatecuratedgallery.carddesigns.card_design import CardDesign


class CardDesigns(Entity):
    """"""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.CardDesigns"

    def add(
        self, description: str, id_: UUID, serialized_properties: str, show_in_toolbox: bool, title: str
    ) -> ClientResult[CardDesign]:
        """Add operation.

        Args:
            description (str): description parameter
            id_ (UUID): id parameter
            serialized_properties (str): serializedProperties parameter
            show_in_toolbox (bool): showInToolbox parameter
            title (str): title parameter
        """
        return_type = ClientResult(self.context, CardDesign())
        qry = ServiceOperationQuery(
            self,
            "Add",
            None,
            {
                "description": description,
                "id": id_,
                "serializedProperties": serialized_properties,
                "showInToolbox": show_in_toolbox,
                "title": title,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type
