from office365.delta_collection import DeltaCollection
from office365.outlook.contacts.folders.folder import ContactFolder
from office365.runtime.client_request_exception import ClientRequestException, DuplicatedObjectException


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

    def get_or_add(self, display_name: str) -> ContactFolder:
        """Gets existing group by name or creates a new one (idempotent)."""
        return_type = self.add(display_name)

        def _on_name_exists(error: ClientRequestException):
            if not isinstance(error, DuplicatedObjectException):
                raise error
            self.get_by_name(display_name).after_execute(
                lambda existing: return_type.copy_from(existing), execute_first=True
            )

        return_type.on_error(_on_name_exists)
        return return_type

    def get_by_name(self, display_name: str) -> ContactFolder:
        """Returns the group with the specified name."""
        return self.single(f"displayName eq '{display_name}'")
