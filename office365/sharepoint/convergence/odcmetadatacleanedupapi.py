from office365.sharepoint.entity import Entity


class OdcMetadataCleanedUpApi(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Convergence.OdcMetadataCleanedUpApi"
