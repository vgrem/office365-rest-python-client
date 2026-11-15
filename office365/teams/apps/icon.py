from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.common.teamwork_hosted_content import TeamworkHostedContent


@version("beta")
class TeamsAppIcon(Entity):
    @odata(name="webUrl")
    @property
    def web_url(self) -> Optional[str]:
        """Gets the webUrl property"""
        return self.properties.get("webUrl", None)

    @odata(name="hostedContent", navigation=True)
    @property
    def hosted_content(self) -> TeamworkHostedContent:
        """Gets the hostedContent property"""
        from office365.common.teamwork_hosted_content import TeamworkHostedContent

        return self.properties.get(
            "hostedContent", TeamworkHostedContent(self.context, ResourcePath("hostedContent", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamsAppIcon"
