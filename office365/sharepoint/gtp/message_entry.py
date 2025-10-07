from office365.runtime.client_value import ClientValue


class MessageEntry(ClientValue):
    """"""

    def __init__(self, content=None, role: str = None):
        """
        :param str content:
        """
        self.content = content
        self.Role = role

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.MessageEntry"
