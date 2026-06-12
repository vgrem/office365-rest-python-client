from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    TypeVar,
)

from typing_extensions import Self

from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.client_value import ClientValue
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.odata.json_format import ODataJsonFormat
from office365.runtime.odata.query_options import QueryOptions
from office365.runtime.odata.v3.json_light_format import JsonLightFormat
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import _ODATA_MARKER
from office365.runtime.utilities import parse_datetime, parse_enum

if TYPE_CHECKING:
    from office365.runtime.client_object_collection import ClientObjectCollection


ClientObjectT = TypeVar("ClientObjectT", bound="ClientObject")


class ClientObject:
    """Base client object which defines named properties and relationships of an entity."""

    _odata_meta: dict[str, str] = {}

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        meta: dict[str, str] = {}
        persist: list[str] = []
        for attr_name, attr in cls.__dict__.items():
            target = attr.fget if isinstance(attr, property) else attr
            m = getattr(target, _ODATA_MARKER, None)
            if m is not None:
                meta[m.name] = attr_name
                if m.persist:
                    persist.append(m.name)
        cls._odata_meta = meta
        cls._odata_persist = persist

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
        self._changes: set[str] = set(getattr(type(self), "_odata_persist", []))
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
        Removes this object from its parent collection, if one exists.

        Returns:
            The current instance for method chaining
        """
        if self._parent_collection is not None:
            self._parent_collection.remove_child(self)
        return self

    def clear_state(self) -> Self:
        """
        Resets the client object's state, clearing any pending changes.

        Returns:
            The current instance for method chaining
        """
        self._properties = {k: v for k, v in self._properties.items() if k not in self._changes}
        self._changes.clear()
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
        """Executes the current set of data retrieval queries and method invocations and retries it if needed.

        Args:
            max_retry (int): Number of times to retry the request
            timeout_secs (int): Seconds to wait before retrying the request.
            success_callback ((office365.runtime.client_object.ClientObject)-> None): A callback to call if
              the request executes successfully.
            failure_callback ((int, requests.exceptions.RequestException)-> None): A callback to call if the request
              fails to execute
            exceptions: tuple of exceptions that we retry
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
        self.context.before_execute(action)
        return self

    def after_execute(
        self,
        action: Callable[[Any], Any],
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

        def _wrapped(result):
            action(result if include_response else self)

        self.context.after_execute(_wrapped, execute_first, include_response)
        return self

    def on_error(self, action: Callable[[ClientRequestException], None], once: bool = True) -> Self:
        self.context.on_error(action, once)
        return self

    def copy_from(self, other: ClientObject) -> Self:
        """Copies all properties from the other object into this one."""
        for k, v in other._properties.items():
            self.set_property(k, v)
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

        Resolves JSON keys to Python properties via ``@odata`` declaration on the
        property method. Falls back to attribute name normalization for backwards
        compatibility.

        Args:
            name: The property name
            default_value: Default value if property doesn't exist

        Returns:
            The property value or default value
        """
        if default_value is None:
            odata_meta = type(self)._odata_meta
            if name in odata_meta:
                return getattr(self, odata_meta[name])
            normalized_name = name[0].lower() + name[1:]
            default_value = getattr(self, normalized_name, None)
        return self._properties.get(name, default_value)

    def set_property(self, name: str, value: Any, persist_changes: bool = True) -> Self:
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
            self._changes.add(name)

        typed_value = self.get_property(name)
        if isinstance(typed_value, (ClientObject, ClientValue)):
            if isinstance(value, list):
                [typed_value.set_property(str(i), v, persist_changes) for i, v in enumerate(value)]
                self._properties[name] = typed_value
            elif isinstance(value, dict):
                [typed_value.set_property(k, v, persist_changes) for k, v in value.items()]
                self._properties[name] = typed_value
            else:
                self._properties[name] = value
        elif isinstance(typed_value, datetime):
            self._properties[name] = parse_datetime(value)
        elif isinstance(typed_value, Enum):
            if value is None:
                self._properties[name] = typed_value
            else:
                self._properties[name] = parse_enum(type(typed_value), value)
        else:
            self._properties[name] = value
        return self

    def ensure_property(self, name: str) -> Self:
        """Ensures a property is loaded before executing an action."""
        return self.ensure_properties([name])

    def ensure_properties(self, names: List[str]) -> Self:
        """Ensures multiple properties are loaded before executing an action."""
        if self.property_ref_name is not None and self.property_ref_name not in names:
            names.append(self.property_ref_name)

        names_to_include = [n for n in names if not self.is_property_available(n)]
        if names_to_include:
            from office365.runtime.queries.read_entity import ReadEntityQuery

            qry = ReadEntityQuery[ClientObject](self, names_to_include)
        else:
            from office365.runtime.queries.noop import NoOpQuery

            qry = NoOpQuery(self.context, self)
        self.context.add_query(qry)
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
        return {k: self.get_property(k) for k in self._changes if k in self._properties}

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
            include_control_info = False
            json = {k: self.get_property(k) for k in self._properties}
        else:
            include_control_info = self.entity_type_name is not None and json_format.include_control_information
            json = {k: self.get_property(k) for k in self._changes if k in self._properties}
        for k, v in json.items():
            if isinstance(v, (ClientObject, ClientValue)):
                json[k] = v.to_json(json_format)
            elif isinstance(v, Enum):
                json[k] = v.value
            elif isinstance(v, datetime):
                json[k] = v.isoformat()

        if json and include_control_info:
            if isinstance(json_format, JsonLightFormat):
                json[json_format.metadata_type] = {"type": self.entity_type_name}
            elif isinstance(json_format, ODataJsonFormat):
                json[json_format.metadata_type] = "#" + self.entity_type_name
        return json
