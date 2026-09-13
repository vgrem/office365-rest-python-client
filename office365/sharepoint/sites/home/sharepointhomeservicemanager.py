from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.function import FunctionQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.publishing.acronyminformation import AcronymInformation
from office365.sharepoint.publishing.textvaluewithlanguage import TextValueWithLanguage


class SharePointHomeServiceManager(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.Publishing.SharePointHomeServiceManager"

    def get_acronyms_and_colors(
        self, labels: ClientValueCollection[TextValueWithLanguage]
    ) -> ClientResult[ClientValueCollection[AcronymInformation]]:
        """GetAcronymsAndColors operation.

        Args:
            labels (ClientValueCollection[TextValueWithLanguage]): labels parameter
        """
        return_type = ClientResult(self.context, ClientValueCollection[AcronymInformation]())
        qry = FunctionQuery(self, "GetAcronymsAndColors", [labels], return_type)
        self.context.add_query(qry)
        return return_type
