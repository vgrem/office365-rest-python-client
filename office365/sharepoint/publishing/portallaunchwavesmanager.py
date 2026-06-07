from office365.sharepoint.entity import Entity


class PortalLaunchWavesManager(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.Publishing.PortalLaunch.PortalLaunchWavesManager"
