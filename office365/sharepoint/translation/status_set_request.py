from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.translation.requested_translation import RequestedTranslation


class TranslationStatusSetRequest(ClientValue):

    def __init__(
        self,
        values=None,
        requested_translations: ClientValueCollection[
            RequestedTranslation
        ] = ClientValueCollection(RequestedTranslation),
    ):
        """
        :param list[RequestedTranslation] values:
        """
        self.RequestedTranslations = ClientValueCollection(RequestedTranslation, values)
        self.RequestedTranslations = requested_translations
