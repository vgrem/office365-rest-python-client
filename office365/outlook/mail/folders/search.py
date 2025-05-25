from typing import Optional

from office365.outlook.mail.folders.folder import MailFolder
from office365.runtime.types.collections import StringCollection


class MailSearchFolder(MailFolder):
    """
    A mailSearchFolder is a virtual folder in the user's mailbox that contains all the email items
    matching specified search criteria. mailSearchFolder inherits from mailFolder.
    Search folders can be created in any folder in a user's Exchange Online mailbox. However, for a search folder
    to appear in Outlook, Outlook for the web, or Outlook Live, the folder must be created in the
    WellKnownFolderName.SearchFolders folder.
    """

    @property
    def filter_query(self):
        # type: () -> Optional[str]
        """The OData query to filter the messages."""
        return self.properties.get("filterQuery", None)

    @property
    def include_nested_folders(self):
        # type: () -> Optional[bool]
        """Indicates how the mailbox folder hierarchy should be traversed in the search. true means that a deep
        search should be done to include child folders in the hierarchy of each folder explicitly specified in
        sourceFolderIds. false means a shallow search of only each of the folders explicitly specified
        in sourceFolderIds."""
        return self.properties.get("includeNestedFolders", None)

    @property
    def is_supported(self):
        # type: () -> Optional[bool]
        """Indicates whether a search folder is editable using REST APIs."""
        return self.properties.get("isSupported", None)

    @property
    def source_folder_ids(self):
        # type: () -> StringCollection
        """The mailbox folders that should be mined."""
        return self.properties.get("sourceFolderIds", StringCollection())
