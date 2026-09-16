from office365.delta_collection import DeltaCollection
from office365.outlook.contacts.folders.folder import ContactFolder


class ContactFolderCollection(DeltaCollection[ContactFolder]):
    def __init__(self, context, resource_path=None):
        super().__init__(context, ContactFolder, resource_path)

    def add(self, display_name, **kwargs) -> ContactFolder:
        """Add a contact folder.

        Args:
            display_name (str): The contact folder's display name.
        """

        kwargs["displayName"] = display_name
        return super().add(**kwargs)

    def ensure(self, display_name: str) -> ContactFolder:
        """Gets an existing folder by name or creates it (idempotent)."""
        from office365.runtime.queries.get_or_create import create_or_get

        return create_or_get(create=lambda: self.add(display_name), find=lambda: self.get_by_name(display_name))

    def get_by_name(self, display_name: str) -> ContactFolder:
        """Returns the group with the specified name."""
        return self.single(f"displayName eq '{display_name}'")
