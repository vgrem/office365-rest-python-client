from __future__ import annotations

from office365.directory.organizations.layouttemplatetype import LayoutTemplateType
from office365.runtime.client_value import ClientValue


class LoginPageLayoutConfiguration(ClientValue):
    isFooterShown: bool | None = None
    isHeaderShown: bool | None = None
    layoutTemplateType: LayoutTemplateType = LayoutTemplateType.default

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.LoginPageLayoutConfiguration"
