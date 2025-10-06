from office365.runtime.client_value import ClientValue


class RepostPageFieldsData(ClientValue):

    @property
    def entity_type_name(self):
        return "SP.Publishing.RepostPageFieldsData"
