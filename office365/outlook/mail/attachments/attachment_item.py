import os

from office365.outlook.mail.attachments.type import AttachmentType
from office365.runtime.client_value import ClientValue


class AttachmentItem(ClientValue):
    """Represents attributes of an item to be attached."""

    def __init__(self, attachment_type: AttachmentType = None, name: str = None, size: int = None):
        """
        :param AttachmentType attachment_type:
        :param str name:
        :param int size:
        """
        super().__init__()
        self.attachmentType = attachment_type
        self.name = name
        self.size = size

    @staticmethod
    def create_file(path: str) -> "AttachmentItem":
        file_name = os.path.basename(path)
        file_size = os.stat(path).st_size
        from office365.outlook.mail.attachments.type import AttachmentType

        return AttachmentItem(attachment_type=AttachmentType.file, name=file_name, size=file_size)
