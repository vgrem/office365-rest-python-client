from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class FileCreationInformation(ClientValue):
    """Represents properties that can be set when creating a file by using the FileCollection.Add method.

    Fields:
        url (str | None): Specifies the URL of the file to be added. It MUST NOT be NULL. It MUST be a URL
            of relative or absolute form. Its length MUST be equal to or greater than 1.
        overwrite (bool): Specifies whether to overwrite an existing file with the same name and in the same
            location as the one being added.
        content (str | bytes | None): Specifies the binary content of the file to be added.
    """

    url: str | None = None
    overwrite: bool = False
    content: str | bytes | None = None
    xor_hash: str | None = None

    def to_json(self, json_format=None):
        return {"overwrite": self.overwrite, "url": self.url}

    @property
    def entity_type_name(self):
        return None
