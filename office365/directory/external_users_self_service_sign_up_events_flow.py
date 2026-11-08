from __future__ import annotations

from office365.directory.authentication.attributecollection.handler import OnAttributeCollectionHandler
from office365.directory.authentication.attributecollection.method_load_start_handler import (  # noqa: E501
    OnAuthenticationMethodLoadStartHandler,
)
from office365.directory.authentication.attributecollection.start_handler import OnAttributeCollectionStartHandler
from office365.directory.authentication.attributecollection.submit_handler import OnAttributeCollectionSubmitHandler
from office365.directory.identities.on_interactive_auth_flow_start_handler import OnInteractiveAuthFlowStartHandler
from office365.directory.identities.on_user_create_start_handler import OnUserCreateStartHandler
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class ExternalUsersSelfServiceSignUpEventsFlow(Entity):
    @odata(name="onAttributeCollection")
    @property
    def on_attribute_collection(self) -> OnAttributeCollectionHandler:
        """Gets the onAttributeCollection property"""
        return self.properties.get("onAttributeCollection", OnAttributeCollectionHandler())

    @odata(name="onAttributeCollectionStart")
    @property
    def on_attribute_collection_start(self) -> OnAttributeCollectionStartHandler:
        """Gets the onAttributeCollectionStart property"""
        return self.properties.get("onAttributeCollectionStart", OnAttributeCollectionStartHandler())

    @odata(name="onAttributeCollectionSubmit")
    @property
    def on_attribute_collection_submit(self) -> OnAttributeCollectionSubmitHandler:
        """Gets the onAttributeCollectionSubmit property"""
        return self.properties.get("onAttributeCollectionSubmit", OnAttributeCollectionSubmitHandler())

    @odata(name="onAuthenticationMethodLoadStart")
    @property
    def on_authentication_method_load_start(self) -> OnAuthenticationMethodLoadStartHandler:
        """Gets the onAuthenticationMethodLoadStart property"""
        return self.properties.get("onAuthenticationMethodLoadStart", OnAuthenticationMethodLoadStartHandler())

    @odata(name="onInteractiveAuthFlowStart")
    @property
    def on_interactive_auth_flow_start(self) -> OnInteractiveAuthFlowStartHandler:
        """Gets the onInteractiveAuthFlowStart property"""
        return self.properties.get("onInteractiveAuthFlowStart", OnInteractiveAuthFlowStartHandler())

    @odata(name="onUserCreateStart")
    @property
    def on_user_create_start(self) -> OnUserCreateStartHandler:
        """Gets the onUserCreateStart property"""
        return self.properties.get("onUserCreateStart", OnUserCreateStartHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ExternalUsersSelfServiceSignUpEventsFlow"
