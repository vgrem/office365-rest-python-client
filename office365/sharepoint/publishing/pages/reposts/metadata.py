from office365.sharepoint.publishing.pages.metadata import SitePageMetadata


class RepostPageMetadata(SitePageMetadata):
    """"""

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "SP.Publishing.RepostPageMetadata"
