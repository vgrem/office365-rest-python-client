"""Generation pipeline: read model, filter types, build, validate and save."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from generator.build.type import TypeBuilder
from generator.checkpoint.manifest import (
    Manifest,
    MetadataChanges,
    diff_members,
    is_up_to_date,
    manifest_path,
    metadata_fingerprint,
    run_signature,
    schema_members,
)
from generator.checkpoint.reporting import Reporter
from generator.checkpoint.verification import PostCommitVerifier, semantic_issues
from generator.core.config import GeneratorOptions
from generator.core.log import log
from generator.edit.validation import ValidationError, validate_source
from generator.metadata.documentation.base import DocumentationProvider
from generator.odata.model import ODataModel
from generator.planning.filters import TypeFilter
from generator.planning.plan import PlanBuilder, _qualified_types


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
        self._filter = TypeFilter.from_options(options)
        context = options.builder_context()
        self._plan = PlanBuilder.build(model, options, self._filter, context)
        self._builder_context = self._plan.apply(context)
        self._output_root = Path(options.output_path).resolve()
        self._reporter = Reporter(self._metadata_path, report_path, options.dry_run)
        self._verifier = PostCommitVerifier(self._output_root, smoke=smoke, check=check)

    def run(self) -> None:
        """Build, validate and (unless dry-run) commit every in-scope type."""
        if self._can_skip():
            log.info("Model is up to date (metadata and config unchanged); nothing to do.")
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
            log.info(f"[{count}/{total}] Processing: {name}")
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
            log.info(f"  Unusable --type {name}: {reason}")

    def _start_at_index(self) -> int:
        """Digit ``start_at``: begin N types into the metadata order."""
        start_at = self._filter.start_at
        if not start_at.isdigit() or int(start_at) <= 0:
            return 0
        log.info(f"  Skipping first {start_at} types (start_at={start_at})")
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
            log.warning(f"Failed on {name}: {e}")
            raise

    def _commit(self, planned: list[tuple[str, TypeBuilder]]) -> None:
        if self._options.dry_run:
            for _, builder in planned:
                log.info(f"  [dry-run] {builder.status}: {builder.file}")
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
