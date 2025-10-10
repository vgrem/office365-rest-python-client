from office365.runtime.client_value import ClientValue


class SmtpServer(ClientValue):

    def __init__(self, value=None, is_readonly=None, is_read_only: bool = None):
        """
        :param str value:
        :param bool is_readonly:
        """
        self.Value = value
        self.IsReadOnly = is_readonly
        self.IsReadOnly = is_read_only

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SmtpServer"
