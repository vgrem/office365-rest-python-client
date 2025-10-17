from __future__ import annotations

import datetime
from enum import Enum
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    TypeVar,
    Union,
)

from requests import Response
from typing_extensions import Self

from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.client_value import ClientValue
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.odata.json_format import ODataJsonFormat
from office365.runtime.odata.query_options import QueryOptions
from office365.runtime.odata.v3.json_light_format import JsonLightFormat
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.utilities import parse_datetime, parse_enum

if TYPE_CHECKING:
    from office365.runtime.client_object_collection import ClientObjectCollection


T = TypeVar("T", bound="ClientObject")


class ClientObject:
    """Base client object which defines named properties and relationships of an entity."""

    def __init__(
        self,
        context: ClientRuntimeContext,
        resource_path: Optional[ResourcePath] = None,
        parent_collection: Optional[ClientObjectCollection] = None,
    ) -> None:
        """
        Initialize a new ClientObject instance.

        Args:
            context: The runtime context for executing operations
            resource_path: The path to this resource in the API
            parent_collection: The collection that contains this object
        """
        self._properties: dict[str, Any] = {}
        self._properties_to_persist: list[str] = []
        self._query_options = QueryOptions()
        self._parent_collection = parent_collection
        self._context = context
        self._entity_type_name: Optional[str] = None
        self._resource_path = resource_path

    def add_to_parent_collection(self) -> Self:
        """
        Adds this object to its parent collection.

        Returns:
            The current instance for method chaining

        Raises:
            ValueError: If no parent collection exists
        """
        if self._parent_collection is None:
            raise ValueError("Cannot add to parent collection: no parent collection exists")

        if self._resource_path is None:
            self._resource_path = ResourcePath(None, self._parent_collection.resource_path)
        self._parent_collection.add_child(self)
        return self

    def remove_from_parent_collection(self) -> Self:
        """
        Removes this object from its parent collection.

        Returns:
            The current instance for method chaining

        Raises:
            ValueError: If no parent collection exists
        """
        if self._parent_collection is None:
            raise ValueError("Cannot remove from parent collection: no parent collection exists")
        self._parent_collection.remove_child(self)
        return self

    def clear_state(self) -> Self:
        """
        Resets the client object's state, clearing any pending changes.

        Returns:
            The current instance for method chaining
        """
        self._properties = {k: v for k, v in self._properties.items() if k not in self._properties_to_persist}
        self._properties_to_persist = []
        self._query_options = QueryOptions()
        return self

    def execute_query(self) -> Self:
        """
        Submits all pending requests to the server.

        Returns:
            The current instance for method chaining
        """
        self.context.execute_query()
        return self

    def execute_query_retry(
        self,
        max_retry: int = 5,
        timeout_secs: int = 5,
        success_callback=None,
        failure_callback=None,
        exceptions=(ClientRequestException,),
    ):
        """
        Executes the current set of data retrieval queries and method invocations and retries it if needed.

        :param int max_retry: Number of times to retry the request
        :param int timeout_secs: Seconds to wait before retrying the request.
        :param (office365.runtime.client_object.ClientObject)-> None success_callback: A callback to call
            if the request executes successfully.
        :param (int, requests.exceptions.RequestException)-> None failure_callback: A callback to call if the request
            fails to execute
        :param exceptions: tuple of exceptions that we retry
        """
        self.context.execute_query_retry(
            max_retry=max_retry,
            timeout_secs=timeout_secs,
            success_callback=success_callback,
            failure_callback=failure_callback,
            exceptions=exceptions,
        )
        return self

    def before_execute(self, action: Callable[[RequestOptions], None]) -> Self:
        """
        Attaches an event handler that runs before query execution.

        Args:
            action: The callback function to execute

        Returns:
            The current instance for method chaining
        """
        self.context.before_query_execute(action)
        return self

    def after_execute(
        self,
        action: Callable[[Self | Response], None],
        execute_first: bool = False,
        include_response: bool = False,
    ) -> Self:
        """
        Attaches an event handler that runs after query execution.

        Args:
            action: The callback function to execute
            execute_first: Whether this handler should run before others
            include_response: Whether to include the raw response

        Returns:
            The current instance for method chaining
        """
        self.context.after_query_execute(action, execute_first, include_response)
        return self

    def get(self) -> Self:
        """
        Retrieves the client object's data from the server.

        Returns:
            The current instance for method chaining
        """
        self.context.load(self)
        return self

    def is_property_available(self, name: str) -> bool:
        """
        Checks if a property has been retrieved or set.

        Args:
            name: The property name to check

        Returns:
            True if the property is available, False otherwise
        """
        if name in self.properties:
            return True
        return False

    def expand(self, names: List[str]) -> Self:
        """
        Specifies related resources to include in the response.

        Args:
            names: List of related resource names to expand

        Returns:
            The current instance for method chaining
        """
        self.query_options.expand = names
        return self

    def select(self, names: List[str]) -> Self:
        """
        Specifies which properties to include in the response.

        Args:
            names: List of property names to select

        Returns:
            The current instance for method chaining
        """
        self.query_options.select = names
        return self

    def get_property(self, name: str, default_value: Any = None) -> Any:
        """
        Gets the value of a property.

        Args:
            name: The property name
            default_value: Default value if property doesn't exist

        Returns:
            The property value or default value
        """
        if default_value is None:
            normalized_name = name[0].lower() + name[1:]
            default_value = getattr(self, normalized_name, None)
        return self._properties.get(name, default_value)

    def set_property(self, name: Union[str, int], value: Any, persist_changes: bool = True) -> Self:
        """
        Sets the value of a property.

        Args:
            name: The property name
            value: The value to set
            persist_changes: Whether to mark the property for persistence

        Returns:
            The current instance for method chaining
        """
        if persist_changes:
            self._properties_to_persist.append(name)

        typed_value = self.get_property(name)
        if isinstance(typed_value, (ClientObject, ClientValue)):
            if isinstance(value, list):
                [typed_value.set_property(i, v, persist_changes) for i, v in enumerate(value)]
                self._properties[name] = typed_value
            elif isinstance(value, dict):
                [typed_value.set_property(k, v, persist_changes) for k, v in value.items()]
                self._properties[name] = typed_value
            else:
                self._properties[name] = value
        else:
            if isinstance(typed_value, datetime.datetime):
                self._properties[name] = parse_datetime(value)
            elif isinstance(typed_value, Enum):
                self._properties[name] = parse_enum(type(typed_value), value)
            else:
                self._properties[name] = value
        return self

    def ensure_property(self, name: str, action: Callable[..., None], *args: Any, **kwargs: Any) -> Self:
        """
        Ensures a property is loaded before executing an action.

        Args:
            name: The property name to ensure
            action: The callback to execute after ensuring
            *args: Positional arguments for the callback
            **kwargs: Keyword arguments for the callback

        Returns:
            The current instance for method chaining
        """
        return self.ensure_properties([name], action, *args, **kwargs)

    def ensure_properties(self, names: List[str], action: Callable[..., None], *args: Any, **kwargs: Any) -> Self:
        """
        Ensures multiple properties are loaded before executing an action.

        Args:
            names: List of property names to ensure
            action: The callback to execute after ensuring
            *args: Positional arguments for the callback
            **kwargs: Keyword arguments for the callback

        Returns:
            The current instance for method chaining
        """
        if self.property_ref_name is not None and self.property_ref_name not in names:
            names.append(self.property_ref_name)

        names_to_include = [n for n in names if not self.is_property_available(n)]
        if len(names_to_include) > 0:
            from office365.runtime.queries.read_entity import ReadEntityQuery

            qry = ReadEntityQuery(self, names_to_include)

            def _after_loaded(return_type):
                action(*args, **kwargs)

            self.context.add_query(qry).after_query_execute(_after_loaded)
        else:
            action(*args, **kwargs)
        return self

    @property
    def entity_type_name(self) -> str:
        """
        Gets the server type name for this entity.

        Returns:
            The entity type name
        """
        if self._entity_type_name is None:
            self._entity_type_name = type(self).__name__
        return self._entity_type_name

    @property
    def property_ref_name(self) -> Optional[str]:
        """Returns property reference name"""
        return None

    @property
    def resource_url(self) -> Optional[str]:
        """
        Gets the full resource URL for this object.

        Returns:
            The full URL or None if path isn't set
        """
        if self.resource_path is None:
            return None
        return self.context.service_root_url + str(self.resource_path)

    @property
    def context(self) -> ClientRuntimeContext:
        """
        Gets the runtime context for this object.

        Returns:
            The runtime context
        """
        return self._context

    @property
    def resource_path(self) -> Optional[ResourcePath]:
        """
        Gets the resource path for this object.

        Returns:
            The resource path
        """
        return self._resource_path

    @property
    def query_options(self) -> QueryOptions:
        """
        Gets the OData query options for this object.

        Returns:
            The query options
        """
        return self._query_options

    @property
    def properties(self) -> Dict[str, Any]:
        """
        Gets all properties of this object.

        Returns:
            Dictionary of property names and values
        """
        return self._properties

    @property
    def persistable_properties(self):
        return {k: self.get_property(k) for k in self._properties_to_persist if k in self._properties}

    @property
    def parent_collection(self) -> Optional[ClientObjectCollection]:
        """
        Gets the parent collection of this object.

        Returns:
            The parent collection or None
        """
        return self._parent_collection

    def to_json(self, json_format: Optional[ODataJsonFormat] = None) -> Dict[str, Any]:
        """
        Serializes the client object to a JSON-compatible dictionary.

        Args:
            json_format: The OData JSON format settings

        Returns:
            Dictionary representing the serialized object
        """
        if json_format is None:
            ser_prop_names = [n for n in self._properties.keys()]
            include_control_info = False
        else:
            ser_prop_names = [n for n in self._properties_to_persist]
            include_control_info = self.entity_type_name is not None and json_format.include_control_information

        json = {k: self.get_property(k) for k in self._properties if k in ser_prop_names}
        for k, v in json.items():
            if isinstance(v, (ClientObject, ClientValue)):
                json[k] = v.to_json(json_format)
            elif isinstance(v, Enum):
                json[k] = v.value

        if json and include_control_info:
            if isinstance(json_format, JsonLightFormat):
                json[json_format.metadata_type] = {"type": self.entity_type_name}
            elif isinstance(json_format, ODataJsonFormat):
                json[json_format.metadata_type] = "#" + self.entity_type_name
        return json
