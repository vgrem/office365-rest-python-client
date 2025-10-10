from office365.runtime.client_value import ClientValue


class CExternalSharingEnforcement(ClientValue):

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Sharing.Internal.CExternalSharingEnforcement"
