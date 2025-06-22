from office365.runtime.client_value import ClientValue


class DirectorySessionData(ClientValue):

    @property
    def entity_type_name(self) -> str:
        return "SP.Directory.Provider.DirectorySessionData"
