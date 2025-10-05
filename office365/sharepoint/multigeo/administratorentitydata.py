from office365.runtime.client_value import ClientValue


class GeoAdministratorEntityData(ClientValue):

    def __init__(
        self,
        display_name: str = None,
        login_name: str = None,
        member_type: int = None,
        object_id: str = None,
    ):
        self.DisplayName = display_name
        self.LoginName = login_name
        self.MemberType = member_type
        self.ObjectId = object_id

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.GeoAdministratorEntityData"
