"""What a package has, asked once instead of rescanning its source from every caller.

A declaration lives on the function it describes (:mod:`office365.permissions.declaration`),
so any single call can be asked what it needs without this module. A *whole-package* question
- which operations build a request, which of them name nothing - is different: it needs every
module imported and every member looked at, and doing that in a test, a report and a ledger
means three walks that disagree at the edges.

So the walk happens here, once per package and process, and answers three questions:

:meth:`Index.declared`
    what the package promises, as operations;
:meth:`Index.undeclared`
    which operations build a request and name nothing - the debt a ratchet records;
:meth:`Index.debt`
    the same, counted per service package, which is the shape a ratchet stores.

Nothing registers itself: a class or a method does not tell this module that it exists, which
is why the answer cannot depend on the order a process happened to import things in.
"""

from __future__ import annotations

import importlib
import inspect
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from types import CodeType, ModuleType
from typing import TYPE_CHECKING, Any, Callable, Iterator, Optional, Sequence, cast

if TYPE_CHECKING:
    from office365.permissions.declaration import PermissionRequirement

#: The calls that put a query on the wire. A method that makes one issues a request; a method
#: that only constructs a query and hands it back is not counted, so the answer is a floor
#: rather than a census - the safe direction for a debt ledger, since an uncounted request
#: cannot be reported as declared. The async twins count too: a hole in the detector is a hole
#: exactly where an awaitable path would stand.
_SUBMIT = frozenset({"add_query", "execute_query", "execute_batch", "execute_query_async", "execute_batch_async"})

#: Packages that are not asked to name a permission: the transport orchestrates requests that
#: model methods already declare, and a root-level base class cannot know the type it creates
#: (``Entity.get`` serves every entity there is).
UNTRACKED = frozenset({"runtime", "."})


@dataclass(frozen=True)
class Operation:
    """A method, or a module-level function, that issues a request or names a permission."""

    #: The dotted module the operation is defined in, e.g. ``office365.outlook.user``.
    module: str
    #: The class it belongs to, e.g. ``Message``; empty for a module-level function.
    owner: str
    #: The name inside that class or module, e.g. ``send``.
    name: str
    #: What it declares, or ``None`` when it declares nothing.
    declaration: Optional["PermissionRequirement"] = None
    #: Whether its body submits a query.
    issues_request: bool = False

    @property
    def qualname(self) -> str:
        """The name inside its module, e.g. ``Message.send``."""
        return f"{self.owner}.{self.name}" if self.owner else self.name

    @property
    def fqn(self) -> str:
        """The name inside the whole library, e.g. ``office365.outlook.user:User.send``."""
        return f"{self.module}:{self.qualname}"

    @property
    def is_private(self) -> bool:
        """Whether it is an implementation detail rather than an entry point."""
        return self.name.startswith("_")

    @property
    def declares(self) -> bool:
        """Whether it names a permission at all."""
        return self.declaration is not None


@dataclass(frozen=True)
class Index:
    """What one package declares, and what it still leaves unnamed."""

    package: str
    operations: tuple[Operation, ...]

    def declared(self) -> tuple[Operation, ...]:
        """Every operation that names a permission, whether or not it submits a query."""
        return tuple(operation for operation in self.operations if operation.declares)

    def undeclared(self) -> tuple[Operation, ...]:
        """Every operation that submits a query and names nothing."""
        return tuple(operation for operation in self.operations if operation.issues_request and not operation.declares)

    def debt(self) -> dict[str, int]:
        """Undeclared public operations, counted per service package, biggest first.

        Private helpers are left out: they are reached through the method that owns the
        request, and the ledger asks who owns the request, not who typed it.
        """
        counted: dict[str, int] = {}
        for operation in self.undeclared():
            package = _service(operation.module)
            if package in UNTRACKED or operation.is_private:
                continue
            counted[package] = counted.get(package, 0) + 1
        return dict(sorted(counted.items(), key=lambda item: (-item[1], item[0])))


@lru_cache(maxsize=None)
def index(package: ModuleType) -> Index:
    """Every operation of ``package``, read from source once per process.

    Something has to import the tree for a whole-package answer, and this walk is over files
    rather than modules: ``pkgutil.walk_packages`` skips a directory without an
    ``__init__.py``, which is every namespace-package subtree in this library, so an index
    built on it would report less debt than there is.
    """
    operations = [operation for module in _modules(package) for operation in _operations(module)]
    return Index(package=package.__name__, operations=tuple(operations))


def _modules(package: ModuleType) -> Iterator[ModuleType]:
    """Import every module defined by ``package``'s files, including namespace subtrees."""
    for directory in map(Path, package.__path__):
        for path in sorted(directory.rglob("*.py")):
            parts = list(path.relative_to(directory).with_suffix("").parts)
            if parts[-1] == "__init__":
                parts.pop()
            yield importlib.import_module(".".join([package.__name__, *parts]))


def _operations(module: ModuleType) -> Iterator[Operation]:
    """The operations ``module`` defines itself, as opposed to the ones it re-exports."""
    for name, value in vars(module).items():
        if getattr(value, "__module__", None) != module.__name__:
            continue
        if isinstance(value, type):
            for member, func in _members(value):
                operation = _operation(module.__name__, value.__qualname__, member, func)
                if operation is not None:
                    yield operation
        elif inspect.isfunction(value):
            operation = _operation(module.__name__, "", name, value)
            if operation is not None:
                yield operation


def _members(cls: type) -> Iterator[tuple[str, Callable[..., Any]]]:
    """Every function defined in ``cls``, as (name, function), including property getters."""
    for name, member in vars(cls).items():
        func = _function(member)
        if func is not None:
            yield name, func


def _function(member: object) -> Optional[Callable[..., Any]]:
    """The function behind a class member, or ``None`` for a constant or a nested class.

    A property counts: its getter runs when the attribute is read, so a getter that submits a
    query is an operation that issues one, and several collections in the library do exactly
    that (``AuditCoreRoot.records`` and friends).
    """
    if isinstance(member, property):
        member = member.fget
    unwrapped = getattr(member, "__func__", member)
    if not inspect.isfunction(unwrapped):
        # A member only one service root declares is a descriptor, so that naming it answers
        # for the client (``hasattr``) before it is called; the function it carries is still
        # the operation, reached through ``__wrapped__``.
        unwrapped = inspect.unwrap(cast(Callable[..., Any], unwrapped))
    return unwrapped if inspect.isfunction(unwrapped) else None


def _operation(module: str, owner: str, name: str, func: Callable[..., Any]) -> Optional[Operation]:
    """The operation a function describes, or ``None`` when nobody would ask about it."""
    declaration = getattr(func, "__required_permissions__", None)
    issues_request = _submits(func)
    if declaration is None and not issues_request:
        return None
    return Operation(
        module=module,
        owner=owner,
        name=name,
        declaration=declaration,
        issues_request=issues_request,
    )


def _submits(func: Callable[..., Any]) -> bool:
    """Whether calling this function submits a query, judged from the names in its bytecode.

    The declaration is read off the wrapper while the body that builds the request is the
    wrapped function, so a decorated method is unwrapped first. Nested code objects are
    followed, because a method may build its query inside a closure or a comprehension.
    """
    code = getattr(inspect.unwrap(func), "__code__", None)
    return code is not None and any(_SUBMIT.intersection(frame.co_names) for frame in _codes(code))


def _codes(code: CodeType) -> Sequence[CodeType]:
    """``code`` plus every nested one, so a query built inside a closure still counts."""
    nested = [value for value in code.co_consts if isinstance(value, CodeType)]
    return [code, *(inner for child in nested for inner in _codes(child))]


def _service(module: str) -> str:
    """The service package a module belongs to: ``outlook``, ``sharepoint``, or ``.``."""
    parts = module.split(".")
    return parts[1] if parts[1:-1] else "."
