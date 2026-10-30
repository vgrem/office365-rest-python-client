from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.authentication.attributecollection.handler import (
        OnAttributeCollectionHandler,
    )
    from office365.directory.authentication.attributecollection.method_load_start_handler import (
        OnAuthenticationMethodLoadStartHandler,
    )
    from office365.directory.authentication.attributecollection.start_handler import (
        OnAttributeCollectionStartHandler,
    )
    from office365.directory.authentication.attributecollection.submit_handler import (
        OnAttributeCollectionSubmitHandler,
    )
    from office365.directory.identities.on_interactive_auth_flow_start_handler import (
        OnInteractiveAuthFlowStartHandler,
    )
    from office365.directory.identities.on_user_create_start_handler import (
        OnUserCreateStartHandler,
    )


class ExternalUsersSelfServiceSignUpEventsFlow(Entity):
    @odata(name="onAttributeCollection")
    @property
    def on_attribute_collection(self) -> OnAttributeCollectionHandler:
        """Gets the onAttributeCollection property"""
        from office365.directory.authentication.attributecollection.handler import (
            OnAttributeCollectionHandler,
        )

        return self.properties.get("onAttributeCollection", OnAttributeCollectionHandler())

    @odata(name="onAttributeCollectionStart")
    @property
    def on_attribute_collection_start(self) -> OnAttributeCollectionStartHandler:
        """Gets the onAttributeCollectionStart property"""
        from office365.directory.authentication.attributecollection.start_handler import (
            OnAttributeCollectionStartHandler,
        )

        return self.properties.get("onAttributeCollectionStart", OnAttributeCollectionStartHandler())

    @odata(name="onAttributeCollectionSubmit")
    @property
    def on_attribute_collection_submit(self) -> OnAttributeCollectionSubmitHandler:
        """Gets the onAttributeCollectionSubmit property"""
        from office365.directory.authentication.attributecollection.submit_handler import (
            OnAttributeCollectionSubmitHandler,
        )

        return self.properties.get("onAttributeCollectionSubmit", OnAttributeCollectionSubmitHandler())

    @odata(name="onAuthenticationMethodLoadStart")
    @property
    def on_authentication_method_load_start(self) -> OnAuthenticationMethodLoadStartHandler:
        """Gets the onAuthenticationMethodLoadStart property"""
        from office365.directory.authentication.attributecollection.method_load_start_handler import (
            OnAuthenticationMethodLoadStartHandler,
        )

        return self.properties.get("onAuthenticationMethodLoadStart", OnAuthenticationMethodLoadStartHandler())

    @odata(name="onInteractiveAuthFlowStart")
    @property
    def on_interactive_auth_flow_start(self) -> OnInteractiveAuthFlowStartHandler:
        """Gets the onInteractiveAuthFlowStart property"""
        from office365.directory.identities.on_interactive_auth_flow_start_handler import (
            OnInteractiveAuthFlowStartHandler,
        )

        return self.properties.get("onInteractiveAuthFlowStart", OnInteractiveAuthFlowStartHandler())

    @odata(name="onUserCreateStart")
    @property
    def on_user_create_start(self) -> OnUserCreateStartHandler:
        """Gets the onUserCreateStart property"""
        from office365.directory.identities.on_user_create_start_handler import (
            OnUserCreateStartHandler,
        )

        return self.properties.get("onUserCreateStart", OnUserCreateStartHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ExternalUsersSelfServiceSignUpEventsFlow"
