from office365.runtime.client_value import ClientValue


class AttachmentCreationInformation(ClientValue):
    def __init__(self, filename: str = None, content: bytes = None):
        """
        Represents properties that can be set when creating a file by using the AttachmentFiles.Add method.

        :param str filename: Specifies the file name of the list item attachment.
        :param str or bytes content: The contents of the file as a stream.
        """
        super(AttachmentCreationInformation, self).__init__()
        self.filename = filename
        self.content = content
