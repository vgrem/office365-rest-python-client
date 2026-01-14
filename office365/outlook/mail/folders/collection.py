from office365.delta_collection import DeltaCollection
from office365.outlook.mail.folders.folder import MailFolder


class MailFolderCollection(DeltaCollection[MailFolder]):
    """Mail folder's collection"""

    def __init__(self, context, resource_path=None):
        super(MailFolderCollection, self).__init__(context, MailFolder, resource_path)

    def add(self, display_name, is_hidden=False):
        # type: (str, bool) -> MailFolder
        """Use this API to create a new mail folder in the root folder of the user's mailbox.

        If you intend a new folder to be hidden, you must set the isHidden property to true on creation.
        """
        props = {"displayName": display_name, "isHidden": is_hidden}
        return super(MailFolderCollection, self).add(**props)
