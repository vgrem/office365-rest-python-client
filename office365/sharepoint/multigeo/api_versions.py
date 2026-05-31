from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class MultiGeoApiVersions(Entity):
    """"""

    def __init__(self, context, resource_path=None):
        if resource_path is None:
            resource_path = ResourcePath("Microsoft.Online.SharePoint.MultiGeo.Service.MultiGeoApiVersions")
        super().__init__(context, resource_path)

    @odata(name="SupportedVersions")
    @property
    def supported_versions(self) -> StringCollection:
        return self.properties.get("SupportedVersions", StringCollection())

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.MultiGeoApiVersions"
