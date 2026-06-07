from office365.sharepoint.entity import Entity


class IRMigration(Entity):
    """"""

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.IR.IRMigration"
