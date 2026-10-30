"""Generation pipeline: read model, filter types, build, validate and save."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from generator.builders.member import sanitize_member_name
from generator.builders.naming import normalize_member_key
from generator.builders.resolution import TypeRegistry
from generator.builders.type import TypeBuilder
from generator.config import GeneratorOptions
from generator.cycles import find_cyclic_types
from generator.documentation.base import DocumentationProvider
from generator.filters import TypeFilter
from generator.manifest import (
    Manifest,
    MetadataChanges,
    diff_members,
    is_up_to_date,
    manifest_path,
    metadata_fingerprint,
    run_signature,
    schema_members,
)
from generator.odata.model import ODataModel
from generator.reporting import Reporter
from generator.routing import Router, planned_module
from generator.validation import ValidationError, validate_source
from generator.verification import PostCommitVerifier, semantic_issues


def _pollable_types(model: ODataModel) -> frozenset[str]:
    """Entity types that model a long-running/async operation.

    A type is pollable when it or any ancestor in the CSDL base chain is an
    ``*Operation`` entity with a ``status`` property (``LongRunningOperation``,
    ``security.CaseOperation``, ``PrintOperation`` …); subtypes inherit it. Such
    types get the ``PollableOperation`` mixin so ``wait()`` / ``wait_async()``
    work on them.
    """

    def is_operation_with_status(name: str) -> bool:
        schema = model.types.get(name)
        return (
            bool(schema)
            and name.rsplit(".", 1)[-1].endswith("Operation")
            and any(prop.lower() == "status" for prop in schema.Properties)
        )

    def walk(name: str) -> bool:
        seen: set[str] = set()
        while name and name not in seen:
            seen.add(name)
            if is_operation_with_status(name):
                return True
            schema = model.types.get(name)
            name = (getattr(schema, "BaseTypeName", None) or "") if schema else ""
        return False

    return frozenset(
        name for name, schema in model.types.items() if schema.BaseTypeFullName == "EntityType" and walk(name)
    )


def _qualified_types(requested: Iterable[str], model: ODataModel) -> Tuple[Tuple[str, ...], Dict[str, str]]:
    """The model's own spelling of each requested type, and why the rest cannot be used.

    ``--type Event`` and ``--type microsoft.graph.Event`` mean the same thing, and both
    surfaces stayed reachable for a while: the pipeline wanted the qualified name while
    the marker plan accepted the short one, so the same flag worked in one mode and
    silently selected nothing in the other. The metadata decides here, as it does
    everywhere else -- and a short name two types share is reported, never guessed.
    """
    by_short: Dict[str, List[str]] = {}
    for name in model.types:
        by_short.setdefault(name.rsplit(".", maxsplit=1)[-1].lower(), []).append(name)
    qualified: List[str] = []
    unresolved: Dict[str, str] = {}
    for name in requested:
        if name in model.types:
            qualified.append(name)
            continue
        candidates = by_short.get(name.rsplit(".", maxsplit=1)[-1].lower(), [])
        if len(candidates) == 1:
            qualified.append(candidates[0])
        elif candidates:
            unresolved[name] = f"ambiguous, the metadata has {', '.join(sorted(candidates))}"
        else:
            unresolved[name] = "not in metadata"
    return tuple(qualified), unresolved


class GeneratorPipeline:
    """Runs one generation pass over an :class:`ODataModel`.

    The pass is *plan-then-commit*: every in-scope type is built and validated
    in memory first, and files are written only after the whole pass succeeds.
    A failure therefore never leaves a partially updated tree.
    """

    def __init__(
        self,
        model: ODataModel,
        options: GeneratorOptions,
        docs_service: Optional[DocumentationProvider] = None,
        base_dir: Path = Path("."),
        update_only: bool = False,
        only_types: Optional[list[str]] = None,
        report_path: Optional[str] = None,
        force: bool = False,
        smoke: bool = True,
        check: bool = False,
    ) -> None:
        self._model = model
        self._options = options
        self._docs = docs_service
        self._update_only = update_only
        self._requested_types = tuple(only_types or ())
        self._only_types, self._unresolved_types = _qualified_types(self._requested_types, model)
        self._force = force
        self._metadata_path = options.metadata_path
        self._base_dir = base_dir
        self._report_path = report_path
        self._previous = Manifest.load(options.metadata_path, base_dir)
        self._builder_context = options.builder_context()
        self._filter = TypeFilter.from_options(options)
        # Only types this run will actually generate (attached or routed) are
        # importable by name; members referencing the rest are skipped.
        router = Router.from_options(self._builder_context)
        registry = TypeRegistry(options.modules.split(","), namespace=options.namespace)
        known_types: set[str] = set()
        type_modules: dict[str, str] = {}
        for name, schema in model.types.items():
            if not self._filter.in_scope(name, schema):
                continue
            module = planned_module(name, schema, registry, router, options.output_path)
            if module is not None:
                known_types.add(name)
                type_modules[name] = module
        #: First member per in-scope enum, so enum-typed fields planned in this run
        #: default to the first member rather than ``field(default_factory=Enum)``.
        enum_defaults: dict[str, str] = {}
        for name, schema in model.types.items():
            if schema.BaseTypeFullName == "EnumType" and self._filter.in_scope(name, schema):
                enum_defaults[name] = next((sanitize_member_name(m) for m in schema.Members), "")
        self._builder_context = self._builder_context.with_plan(
            known_types=frozenset(known_types),
            type_modules=type_modules,
            cyclic_types=frozenset(find_cyclic_types(model, known_types)),
            enum_defaults=enum_defaults,
            inherited_members=model.inherited_member_names(),
            entity_types=frozenset(
                name for name, schema in model.types.items() if schema.BaseTypeFullName == "EntityType"
            ),
            client_value_types=frozenset(
                name for name in known_types if model.types[name].BaseTypeFullName != "EntityType"
            ),
            pollable_types=_pollable_types(model),
            declared_properties={
                name: frozenset(normalize_member_key(key) for key in keys)
                for name, keys in model.effective_property_names().items()
            },
        )
        self._output_root = Path(options.output_path).resolve()
        self._reporter = Reporter(self._metadata_path, report_path, options.dry_run)
        self._verifier = PostCommitVerifier(self._output_root, smoke=smoke, check=check)

    def run(self) -> None:
        """Build, validate and (unless dry-run) commit every in-scope type."""
        if self._can_skip():
            print("Model is up to date (metadata and config unchanged); nothing to do.")
            return
        # A request that resolved to nothing is still a targeted run: falling back to
        # the whole metadata would answer a mistyped --type by writing every file.
        targeted = bool(self._requested_types)
        total = len(self._only_types) if targeted else len(self._model.types)
        start_at = 0 if targeted else self._start_at_index()
        if targeted:
            self._warn_unknown_types()

        count = 0
        skipped_new = 0
        unrouted: dict[str, str] = {}
        planned: list[tuple[str, TypeBuilder]] = []

        for index, (name, schema) in enumerate(self._model.types.items()):
            if targeted:
                if name not in self._only_types:
                    continue
            elif index < start_at:
                continue
            elif self._filter.before_start(name) or self._filter.should_skip(name, schema):
                continue
            builder = TypeBuilder(schema, self._builder_context, self._docs)
            if builder.skip_reason:
                unrouted[name] = builder.skip_reason
                continue
            if self._update_only and builder.state != "attached":
                skipped_new += 1
                continue
            count += 1
            print(f"[{count}/{total}] Processing: {name}")
            self._build(name, builder)
            if builder.built:
                planned.append((name, builder))

        current_members = schema_members(self._model)
        changes = diff_members(self._previous.members, current_members) if self._previous else MetadataChanges([], {})

        self._commit(planned)
        self._reporter.summary(planned, skipped_new, unrouted)
        self._reporter.metadata_changes(changes)
        if not self._options.dry_run:
            self._verifier.verify(planned)
            Manifest(
                manifest_path(self._metadata_path, self._base_dir),
                metadata_fingerprint(self._metadata_path),
                current_members,
                run_signature(self._options),
            ).save()
        self._reporter.write(planned, unrouted, changes)

    def _can_skip(self) -> bool:
        """True when a previous successful run already covered this exact input."""
        return is_up_to_date(
            self._options,
            self._previous,
            force=self._force,
            targeted=bool(self._requested_types or self._report_path),
        )

    def _warn_unknown_types(self) -> None:
        for name, reason in self._unresolved_types.items():
            print(f"  Unusable --type {name}: {reason}")

    def _start_at_index(self) -> int:
        """Digit ``start_at``: begin N types into the metadata order."""
        start_at = self._filter.start_at
        if not start_at.isdigit() or int(start_at) <= 0:
            return 0
        print(f"  Skipping first {start_at} types (start_at={start_at})")
        return int(start_at)

    def _build(self, name: str, builder: TypeBuilder) -> None:
        """Build and validate a single type in memory (no write)."""
        try:
            builder.build()
            if builder.built:
                source = builder.render()
                issues = validate_source(source, builder.file) + semantic_issues(source, builder.file)
                if issues:
                    raise ValidationError(f"{name}: " + "; ".join(issues))
        except Exception as e:
            print(f"Failed on {name}: {e}")
            raise

    def _commit(self, planned: list[tuple[str, TypeBuilder]]) -> None:
        if self._options.dry_run:
            for _, builder in planned:
                print(f"  [dry-run] {builder.status}: {builder.file}")
            return
        for name, builder in planned:
            if not self._within_output(builder.file):
                raise ValidationError(f"{name}: refusing to write outside the output tree: {builder.file}")
        for _, builder in planned:
            builder.save()

    def _within_output(self, path: str) -> bool:
        try:
            Path(path).resolve().relative_to(self._output_root)
        except ValueError:
            return False
        return True
