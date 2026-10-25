from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class ResourceManifestInformation(Entity):
    @odata(name="RequireJsScriptBlock")
    @property
    def require_js_script_block(self) -> Optional[str]:
        """Gets the RequireJsScriptBlock property"""
        return self.properties.get("RequireJsScriptBlock", None)

    @odata(name="ScenarioMapping")
    @property
    def scenario_mapping(self) -> Optional[dict]:
        """Gets the ScenarioMapping property"""
        return self.properties.get("ScenarioMapping", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.WebControls.ResourceManifestInformation"
