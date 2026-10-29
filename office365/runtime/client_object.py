from __future__ import annotations

from enum import Enum
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Collection,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
)

from typing_extensions import Self

from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.converters.value import (
    coerce_value,
    declared_type,
    serialize_value,
    to_snake_case,
)
from office365.runtime.exceptions import ObjectNotFoundException
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.limits import Limit
from office365.runtime.odata.json_format import JsonProfile, as_held
from office365.runtime.odata.query_options import QueryOptions
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.retry import DEFAULT_RETRY_EXCEPTIONS
from office365.runtime.schema import EMPTY, TypeSchema
from office365.runtime.types.odata_property import PREVIEW, NotSupportedInVersion, request_version


def require_declared_version(name: str, declared: Collection[str], context: Any) -> None:
    """Refuse to build ``name`` on a client whose service root does not declare it.

    One model tree serves both service roots, so a preview-only class is an attribute of
    the tree a stable client sees, and holding the class is not the error -- building one
    is: the request it carries names a path the stable root has no entity for, and the
    service answers 404 rather than naming the version that would have worked. A client
    that names no version (a SharePoint context) is never refused: the declaration states
    a fact about Graph, not a rule about every service.
    """
    if not declared:
        return
    version = request_version(context)
    if version is None or version in declared:
        return
    raise NotSupportedInVersion(name, version, PREVIEW)


if TYPE_CHECKING:
    from office365.runtime.client_object_collection import ClientObjectCollection


ClientObjectT = TypeVar("ClientObjectT", bound="ClientObject")


def _swallow_object_not_found(error: ClientRequestException) -> None:
    """Error handler that suppresses a 404 (:class:`ObjectNotFoundException`).

    Any other failure is re-raised so it still propagates to the caller.
    """
    if not isinstance(error, ObjectNotFoundException):
        raise error


class ClientObject:
    """Base client object which defines named properties and relationships of an entity."""

    #: Everything this type declares: its properties, the projections a request and a
    #: ``$select`` are built from, and its OData name. Built in ``__init_subclass__``, so
    #: ``Contact._schema.readonly`` answers a question about a type without an instance.
    _schema: ClassVar[TypeSchema] = EMPTY

    #: The OData name this class declares (``"microsoft.graph.Event"``), emitted by the
    #: generator. A class-level fact, so name resolution reads it without building an
    #: instance; see :func:`office365.runtime.odata.edm.edm_type_name`.
    _odata_type_name: ClassVar[Optional[str]] = None

    #: Declared OData names this type's own service refuses to project. The fact is per
    #: type, not per property -- ``ShieldAddRoleAssignmentPushdown`` is answered on a
    #: ``ListItem`` and refused on a ``Web`` -- so it is stated by the type that saw the
    #: refusal, and the declaration stays intact for hydration and comparison.
    _unselectable: ClassVar[Tuple[str, ...]] = ()

    #: The service roots whose metadata declares this type, declared by
    #: ``@version(...)`` on the class. Empty -- every hand-written class, and every type
    #: both roots declare -- means all of them. The generator states ``@version("beta")``
    #: on a type only the preview root declares, so an attempt to build one on a stable
    #: client fails here, before it becomes a 404.
    _versions: ClassVar[Collection[str]] = ()

    #: The property that spells this type's identity, declared by ``@key(...)`` on the
    #: class. Empty -- every type whose key is its family's default -- leaves
    #: :attr:`property_ref_name` answering the base class's own spelling, so a class that
    #: states nothing behaves exactly as it did before the declaration existed.
    _key: ClassVar[Sequence[str]] = ()

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        cls._schema = TypeSchema.build(cls)

    @classmethod
    def select_all(cls) -> List[str]:
        """The declared columns of this type: every OData name ``$select`` accepts here.

        A navigation property is left out: the service reaches it through the path,
        not through a projection, and naming one in ``$select`` is an error. So is a
        name the type lists in :attr:`_unselectable`, which is how a type says its
        service answers 400 for a column it nevertheless declares. The names come from
        the same declarations the getters read, so a projection built here cannot spell
        a column differently from the code that consumes it.
        """
        return list(cls._schema.columns)

    @classmethod
    def expand_all(cls) -> List[str]:
        """The declared navigation properties ``$expand`` can reach, as ``select_all()``
        lists the ones ``$select`` accepts.

        A link is not a promise: ``$expand`` on ``Event.extensions`` is refused unless a
        ``$filter`` is supplied, so a declaration may say so and keep the name out of
        here while the link itself stays a navigation.
        """
        return [
            declared.name for declared in cls._schema.properties.values() if declared.navigation and declared.expandable
        ]

    @classmethod
    def odata_name(cls, attr: str) -> str:
        """The OData name of a declared getter, given its Python attribute name.

        Raises:
            AttributeError: when the attribute carries no declaration, naming the
                declared attributes so a typo fails here rather than as ``None``
                further down the read path.
        """
        name = cls._schema.by_attr.get(attr)
        if name is not None:
            return name
        declared = ", ".join(sorted(cls._schema.by_attr))
        raise AttributeError(f"{cls.__name__}.{attr} is not a declared property; declared: {declared}")

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
        self._changes: set[str] = set(type(self)._schema.persistable)
        require_declared_version(type(self).__name__, type(self)._versions, context)
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

        Persist-marked properties are kept so they stay present and are sent
        again on subsequent updates (``persist=True`` means "always include"),
        while explicitly changed, non-persistable props are dropped.
        """
        persistable = self._schema.persistable
        self._properties = {k: v for k, v in self._properties.items() if k not in self._changes or k in persistable}
        self._changes.clear()
        self._query_options = QueryOptions()
        return self

    @classmethod
    def declared_limits(cls) -> Tuple[Limit, ...]:
        """The limits declared on this class and its methods/properties (``@limit``)."""
        return cls._schema.declared_limits()

    def execute_query(self) -> Self:
        """
        Submits all pending requests to the server.

        Returns:
            The current instance for method chaining
        """
        self.context.execute_query()
        return self

    async def execute_query_async(self) -> Self:
        """
        Submits all pending requests to the server without blocking the loop.

        Returns:
            The current instance for method chaining
        """
        await self.context.execute_query_async()
        return self

    def execute_query_retry(
        self,
        max_retry: int = 5,
        timeout_secs: int = 5,
        max_delay=None,
        jitter: bool = True,
        success_callback=None,
        failure_callback=None,
        exceptions=DEFAULT_RETRY_EXCEPTIONS,
        is_retriable=None,
    ) -> Self:
        """Executes the current set of data retrieval queries and method invocations and retries it if needed.

        Args:
            max_retry (int): Number of times to retry the request
            timeout_secs (int): Base delay for exponential backoff (seconds)
            max_delay (int): Optional cap on the exponential delay (seconds)
            jitter (bool): Whether to randomize the delay
            success_callback (callable): A callback to call if the request executes successfully.
            failure_callback (callable): A callback to call if the request fails to execute.
            exceptions (tuple): Tuple of exceptions that we retry.
            is_retriable (callable): Optional predicate deciding whether a caught
                exception is retried. Defaults to transient errors; pass
                ``retry_on(...)`` to also retry otherwise-permanent errors.
        """
        self.context.execute_query_retry(
            max_retry=max_retry,
            timeout_secs=timeout_secs,
            max_delay=max_delay,
            jitter=jitter,
            success_callback=success_callback,
            failure_callback=failure_callback,
            exceptions=exceptions,
            is_retriable=is_retriable,
        )
        return self

    async def execute_query_async_retry(
        self,
        max_retry: int = 5,
        timeout_secs: int = 5,
        max_delay=None,
        jitter: bool = True,
        success_callback=None,
        failure_callback=None,
        exceptions=DEFAULT_RETRY_EXCEPTIONS,
        is_retriable=None,
    ) -> Self:
        """Async counterpart of :meth:`execute_query_retry`.

        Args:
            max_retry (int): Number of times to retry the request
            timeout_secs (int): Base delay for exponential backoff (seconds)
            max_delay (int): Optional cap on the exponential delay (seconds)
            jitter (bool): Whether to randomize the delay
            success_callback (callable): Called if the request executes successfully.
            failure_callback (callable): Called if a retry attempt fails.
            exceptions (tuple): Tuple of exceptions that we retry.
            is_retriable (callable): Optional predicate deciding whether a caught
                exception is retried. Defaults to transient errors.
        """
        await self.context.execute_query_async_retry(
            max_retry=max_retry,
            timeout_secs=timeout_secs,
            max_delay=max_delay,
            jitter=jitter,
            success_callback=success_callback,
            failure_callback=failure_callback,
            exceptions=exceptions,
            is_retriable=is_retriable,
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
            self.set_property(k, v, False)
        return self

    def get(self) -> Self:
        """
        Retrieves the client object's data from the server.

        Returns:
            The current instance for method chaining
        """
        self.context.load(self)
        return self

    def get_or_none(self) -> Self:
        """Queue a read that tolerates a missing entity.

        Deferred exactly like :meth:`get`: nothing is sent until the caller runs
        ``execute_query()``. When the entity exists the object is populated; when
        the server reports it missing (HTTP 404, classified as
        :class:`~office365.runtime.exceptions.ObjectNotFoundException`) the error
        is swallowed and the object is left uninitialized — detect that with
        :attr:`is_loaded` (or a typed property being ``None``):

            user = client.users["missing@contoso.com"].get_or_none().execute_query()
            if not user.is_loaded:
                ...

        Any other failure (authentication, throttling, ...) still propagates.

        Returns:
            The current instance for method chaining
        """
        self.get().on_error(_swallow_object_not_found)
        return self

    def _tolerate_missing(self, enabled: bool = True) -> Self:
        """Mark the most recently queued query as tolerating a 404 (one-shot).

        Shared by the ``ignore_missing`` write helpers (``delete_object`` /
        ``recycle``): the error is swallowed only when it is an
        :class:`ObjectNotFoundException`; any other failure propagates.

        Args:
            enabled: When ``False`` this is a no-op, so callers can forward the
                flag unconditionally.
        """
        if enabled:
            self.on_error(_swallow_object_not_found)
        return self

    @property
    def is_loaded(self) -> bool:
        """Whether the object carries data (from a read or a local property set).

        An object that was never initialized — e.g. a lookup that tolerated a 404
        via :meth:`get_or_none` or an empty :meth:`ClientObjectCollection.first_or_none`
        — has no properties and reports ``False``.
        """
        return len(self._properties) > 0

    def __str__(self) -> str:
        """Return the object's natural label (``displayName``/``name``/``title``).

        Falls back to :meth:`__repr__` when no obvious label is loaded, so
        ``print(obj)`` is always meaningful without reaching for a property.
        """
        for name in ("displayName", "name", "title"):
            value = self._properties.get(name)
            if isinstance(value, str) and value:
                return value
        return self.__repr__()

    def __repr__(self) -> str:
        """Return a bounded ``ClassName(prop=value, …)`` rendering.

        Only already-loaded properties are projected; this never triggers a
        request. Used by ``print``/``repr`` and logging.
        """
        from office365.runtime.display import describe

        return describe(self)

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
        name = type(self)._schema.canonical(name)
        if default_value is None:
            meta = type(self)._schema.properties.get(name)
            if meta is not None:
                return getattr(self, meta.attr)
            normalized_name = name[0].lower() + name[1:]
            default_value = getattr(self, normalized_name, None)
            if default_value is None:
                # Multi-word names (``onlineMeeting``) map to a snake_case getter.
                default_value = getattr(self, to_snake_case(name), None)
        return self._properties.get(name, default_value)

    def set_property(self, name: str, value: Any, persist_changes: bool = True) -> Self:
        """Set a property, coercing the value to its declared type.

        Uses the shared conversion core (``coerce_value``/``declared_type``) so
        deserialization and the CSV/JSON pipeline use the same conversions.

        Args:
            name: The property name
            value: The value to set
            persist_changes: Whether to mark the property for persistence

        Returns:
            The current instance for method chaining
        """
        # A preview response spells a renamed member the preview way; the model holds one
        # name per member, so both spellings land on the same declaration from here on.
        name = type(self)._schema.canonical(name)
        if name == "__odata_type":
            return self
        if persist_changes:
            self._changes.add(name)
        current = self.get_property(name)
        # A getter can return a default enum when nothing is stored yet; that
        # fallback must not drive enum coercion (an unrecognized server value
        # would otherwise be discarded).
        if isinstance(current, Enum) and name not in self._properties:
            current = None
        self._properties[name] = coerce_value(declared_type(type(self), name), value, current, persist_changes)
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
            from office365.runtime.queries.deferred import DeferredOperationQuery

            qry = DeferredOperationQuery(self.context, return_type=self)
        self.context.add_query(qry)
        return self

    @property
    def entity_type_name(self) -> str:
        """
        Gets the server type name for this entity.

        Returns:
            The declared OData type name, or the class name when none is declared.
        """
        if self._odata_type_name is not None:
            return self._odata_type_name
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

    def wire_name(self, name: str) -> str:
        """The name this client's service root spells ``name`` with.

        One model tree serves both roots, and a navigation's path segment is the wire
        name, so a getter that builds a path asks here rather than hard-coding the
        stable spelling: ``AccessPackage.catalog`` is ``catalog`` on v1.0 and
        ``accessPackageCatalog`` on the preview root. A member the client's root does
        not declare raises -- that is the whole gate for reading one.
        """
        return type(self)._schema.wire_name(name, request_version(self.context))

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

    def hydrate(self, payload: Any, profile: Optional[JsonProfile] = None) -> Self:
        """Read this object's content from a payload: the mirror of :meth:`to_json`.

        One direction spells, the other reads, and neither is a procedure: the object
        knows its declarations, the profile knows the dialect, and the payload is all
        that is left over. The object is bound to its context before it is filled, so
        ``Event(context).hydrate(payload)`` reads and chains, and a client with no
        credentials is enough to do it offline.

        ``profile=None`` is the spelling :meth:`to_json` writes with no profile (a
        sidecar: no control information), so ``x.hydrate(y.to_json())`` round-trips.
        A payload that came off the wire needs its own profile: JSON Light wraps an
        entity in ``d``, OData V4 does not, and a wrapped payload read in the wrong
        dialect quietly yields an empty object.

        Everything the payload says becomes this object's own content
        (``persist_changes``): content meant to be posted, not a response that happened
        to arrive. A response is filled the other way, by ``profile.hydrate(self, payload)``,
        because what a service said is not what a caller changed.

        Args:
            payload: The payload to read (an entity, or a list of them)
            profile: The profile that spells the payload; ``None`` for what ``to_json()`` wrote

        Returns:
            This object, so reading and spelling chain.
        """
        (profile or as_held()).hydrate(self, payload, persist_changes=True)
        return self

    def to_json(self, profile: Optional[JsonProfile] = None) -> Dict[str, Any]:
        """
        Serializes the client object to a JSON-compatible dictionary.

        Args:
            profile: The profile that spells the payload. ``None`` keeps the object as the
                model holds it — a response or a sidecar — so nothing the service owns is
                dropped and nothing is wrapped.

        Returns:
            Dictionary representing the serialized object (a collection overrides this to
            answer the list of its members)
        """
        if profile is None:
            json = {k: self.get_property(k) for k in self._properties}
        else:
            version = request_version(self.context)
            persistable, readonly = self._schema.persistable, self._schema.readonly
            declared = self._schema.properties
            # The payload is spelled the way the client's service root spells it, so a
            # renamed member goes out under the name that root declares -- and a member
            # that root does not declare raises instead of being sent into a schema that
            # has no room for it.
            json = {
                self._schema.wire_name(k, version): self.get_property(k)
                for k in self._properties
                if k not in readonly
                and profile.includes(self, declared.get(k), k, k in self._changes or k in persistable)
            }
        # ``__``-prefixed keys are this client's own bookkeeping, ingested from a
        # response (``__etag`` for ``If-Match``, ``__odata_type``, ``__deferred``):
        # they describe the response, never the entity, so no payload carries them.
        # A dialect's control marker (``__metadata``) is added *after* this filter.
        json = {k: serialize_value(v, profile) for k, v in json.items() if not k.startswith("__")}

        return json if profile is None else profile.wrap(self, profile.refine(json, self._schema.properties.values()))
