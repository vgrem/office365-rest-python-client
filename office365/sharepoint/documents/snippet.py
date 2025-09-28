from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.placeholderv2 import PlaceholderV2


class Snippet(ClientValue):

    def __init__(
        self,
        id_: str = None,
        name: str = None,
        placeholders: ClientValueCollection[PlaceholderV2] = ClientValueCollection(
            PlaceholderV2
        ),
        snippet_library_mapped_id: str = None,
        snippet_library_mapped_version: str = None,
    ):
        self.Id = id_
        self.Name = name
        self.Placeholders = placeholders
        self.SnippetLibraryMappedId = snippet_library_mapped_id
        self.SnippetLibraryMappedVersion = snippet_library_mapped_version
