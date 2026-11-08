"""Command line entry point for the model generator."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from generator.checkpoint.manifest import Manifest, is_up_to_date
from generator.cli.session import GENERATOR_DIR, Session, resolve_path
from generator.core.config import ConfigError, GeneratorOptions
from generator.core.log import configure as configure_logging
from generator.core.log import log
from generator.core.services import service_names
from generator.edit.validation import ValidationError
from generator.metadata.documentation.subservices import fetch_service_map, load_service_map, write_service_map
from generator.model_index.resolution import TypeRegistry
from generator.odata.reader import ODataReader
from generator.pipeline import GeneratorPipeline
from generator.planning.filters import TypeFilter
from generator.planning.routing import Router, render_suggestions
from generator.tools.beta_markers import compare_markers, plan_markers, read_declared_markers, read_declared_versions
from generator.tools.beta_markers import write_report as write_marker_report
from generator.tools.entity_keys import KeyPlan, plan_keys
from generator.tools.entity_keys import write_report as write_key_report
from generator.tools.metadata_diff import diff_metadata, write_report

#: The repository root: what a report's file paths are shown relative to.
REPO_ROOT = GENERATOR_DIR.parent


def generate(
    service: str,
    *,
    dry_run: bool = False,
    update_only: bool = False,
    only_types: Optional[Sequence[str]] = None,
    report_path: Optional[str] = None,
    force: bool = False,
    smoke: bool = True,
    check: bool = False,
    metadata: Optional[str] = None,
) -> int:
    """Read the service metadata and generate/update the corresponding model files.

    ``metadata`` reads a different snapshot than the configured one -- the preview CSDL
    -- while the routing, filters and output tree stay exactly what the service config
    says. That is what makes one model possible: the tree is the union, the snapshot
    decides what is new, and the marker pass records which root declares what.

    Returns how many files the run wrote, or would write under ``dry_run``.
    """
    session = Session.open(service, dry_run=dry_run, metadata=metadata)
    definition, options = session.definition, session.options
    if is_up_to_date(
        options,
        Manifest.load(options.metadata_path, GENERATOR_DIR),
        force=force,
        targeted=bool(only_types or report_path),
    ):
        log.info("Model is up to date (metadata and config unchanged); nothing to do.")
        return 0
    reader: ODataReader = definition.reader(options.metadata_path)
    documentation = definition.documentation() if definition.documentation else None
    return GeneratorPipeline(
        reader.read(),
        options,
        documentation,
        base_dir=GENERATOR_DIR,
        update_only=update_only,
        only_types=list(only_types) if only_types else None,
        report_path=report_path,
        force=force,
        smoke=smoke,
        check=check,
    ).run()


def suggest_routing(service: str) -> None:
    """Print a proposed ``routing``/``type_routing`` YAML block for unrouted types."""
    session = Session.open(service)
    options = session.options
    model = session.read_model()
    registry = TypeRegistry(options.modules.split(","), namespace=options.namespace)
    router = Router.from_options(options.builder_context())
    base = TypeFilter.from_options(options)
    # Routing is independent of which kinds are generated: propose placements for
    # every in-scope type, so enabling a new kind (e.g. EntityType) has routes.
    schema_filter = TypeFilter(
        exact_ignored=base.exact_ignored, prefix_ignored=base.prefix_ignored, include_base_types=set(), start_at=""
    )
    print(
        render_suggestions(
            model, schema_filter, registry, router, services=options.services, service_map=load_service_map()
        )
    )


def compare_metadata(
    service: str,
    other_path: str,
    report_path: Optional[str] = None,
    *,
    apply: bool = False,
    only_types: Optional[Sequence[str]] = None,
    dry_run: bool = False,
) -> None:
    """Print what another metadata snapshot declares on top of the configured one.

    The report carries the delta and the ``beta=`` markers it justifies, because the
    second is what a generation pass consumes and the first is how a reviewer checks
    it: every marker in the report is a member the two snapshots disagree about.

    ``apply`` brings the model's own decorators in line with the plan -- adding a
    marker the snapshots now justify, changing one they no longer spell the same way,
    and **removing** one they have stopped justifying (a preview that went stable).
    """
    session = Session.open(service)
    options = session.options
    other = resolve_path(other_path)
    base = session.read_model()
    target = session.read_model(str(other))
    delta = diff_metadata(
        base,
        target,
        base_label=Path(options.metadata_path).name,
        target_label=other.name,
    )
    plan = plan_markers(delta)
    print(delta.render())
    print(f"\n{plan.render()}")
    if report_path:
        write_report(delta, report_path)
        write_marker_report(plan, None, _marker_report_path(report_path))
        log.info(f"\nFull report written to {report_path}")
    if apply:
        _apply_marker_pass(options, plan.restricted(only_types) if only_types else plan, dry_run=dry_run)


def _apply_marker_pass(options: GeneratorOptions, plan, *, dry_run: bool) -> None:
    """Write the markers the plan justifies into the model, and say what it wrote."""
    from generator.tools.marker_apply import TypeFiles, apply_markers

    files = TypeFiles(Path(options.output_path))
    names = [marker.type_name for marker in plan.markers] + [marker.type_name for marker in plan.types]
    sources = {name: files.path_of(name) for name in names}
    known = {name: path for name, path in sources.items() if path is not None}
    declared = read_declared_markers(known)
    # Only a gate something enforces counts as declared: an ``@version`` left on a complex
    # type is a comment claiming to be a rule, and the pass that wrote it must take it back.
    declared_versions = {
        name: versions for name, versions in read_declared_versions(known).items() if files.is_addressed(name)
    }
    report = apply_markers(compare_markers(plan, declared, declared_versions), files, dry_run=dry_run)
    print(f"\n{report.render()}")
    for edit in report.edits:
        print(f"  {edit.action:<7} {Path(edit.path).name}  {edit.type_name.rsplit('.', 1)[-1]}.{edit.member}")
    for marker, reason in report.skipped:
        print(f"  skipped {marker.type_name.rsplit('.', 1)[-1]}.{marker.member}: {reason}")
    if dry_run and report.edits:
        print("\nDry run: no file was written.")


def key_pass(
    service: str,
    *,
    apply: bool,
    only_types: Optional[Sequence[str]] = None,
    report_path: Optional[str] = None,
    dry_run: bool = False,
    metadata: Optional[str] = None,
) -> None:
    """Bring the model's ``@key(...)`` declarations in line with what the snapshot states.

    A key is read from one snapshot, not compared across two, so this is not a
    ``--diff-metadata`` operation: the plan is the snapshot plus what the classes already
    say. Without ``apply`` it only reports -- which is the mode SharePoint uses, because
    its v3 metadata states keys a client cannot address an entity by.
    """
    from generator.tools.marker_apply import TypeFiles, apply_keys

    session = Session.open(service, metadata=metadata)
    definition, options = session.definition, session.options
    if apply and not definition.keys_authoritative:
        raise ConfigError(
            f"{service}: this snapshot states keys a client cannot address an entity by, "
            "so its keys are reported rather than written -- run --plan-keys and review"
        )
    model = session.read_model()
    root = Path(options.output_path)
    files = TypeFiles(root / definition.model_package if definition.model_package else root)
    plan: KeyPlan = plan_keys(
        model,
        files,
        metadata=Path(options.metadata_path).name,
        default=definition.default_key,
        only=only_types,
    )
    print(plan.render())
    if report_path:
        write_key_report(plan, report_path)
        log.info(f"\nFull plan written to {report_path}")
    if not apply:
        _print_key_plan(plan)
        return
    report = apply_keys(plan, files, dry_run=dry_run)
    print(f"\n{report.render()}")
    for edit in report.edits:
        print(f"  {edit.action:<7} {Path(edit.path).name}  {edit.type_name.rsplit('.', 1)[-1]}.{edit.member}")
    for marker, reason in report.skipped:
        print(f"  skipped {marker.type_name.rsplit('.', 1)[-1]}.{marker.member}: {reason}")
    if dry_run and report.edits:
        print("\nDry run: no file was written.")


def _print_key_plan(plan: KeyPlan) -> None:
    """Say what the plan would write, and why it refuses the rest."""
    for marker in plan.markers:
        print(f"  declare {marker.type_name.rsplit('.', 1)[-1]} = {marker.key}")
    for marker, reason in plan.skipped:
        print(f"  skipped {marker.type_name.rsplit('.', 1)[-1]} ({marker.key}): {reason}")


def _marker_report_path(report_path: str) -> str:
    """``delta.json`` -> ``beta_markers.json``, next to it."""
    path = Path(report_path)
    return str(path.with_name("beta_markers" + path.suffix))


def verify_model(package: Optional[str] = None) -> int:
    """Check the rendered model against its declarations; exit 1 on any disagreement."""
    from generator.tools.declarations import declaration_report

    report = declaration_report(Path(package) if package else None)
    print(report.render())
    return 0 if report.ok else 1


def audit_model(
    service: str,
    package: Optional[str] = None,
    report_path: Optional[str] = None,
    fail: bool = False,
) -> int:
    """Measure the rendered model against the metadata it was generated from.

    ``package`` is the tree to read (default: the service's own sub-package), so the
    same report answers for one directory while it is being filled and for the whole
    model once it is.
    """
    from generator.tools.fidelity import DEFAULT_PREFIX, audit, gaps, read_models, render, write_report

    session = Session.open(service)
    model_root = Path(session.options.output_path).resolve()
    root = Path(package).resolve() if package else model_root / session.definition.model_package
    # The whole tree, then the package: a member can be inherited from a class in
    # another package, and the audit has to see it to know the subclass serves it.
    models = [model for model in read_models(model_root, DEFAULT_PREFIX.get(service, "")) if root in model.path.parents]
    findings = audit(
        models,
        session.read_model(),
        ignored_types=session.options.ignored_types,
        ignored_properties=session.options.ignored_properties,
    )
    if report_path:
        write_report(findings, report_path)
    print(render(findings, REPO_ROOT))
    return 1 if fail and gaps(findings) else 0


def fetch_services() -> None:
    """Fetch the Graph docs service taxonomy and cache it for --suggest-routing."""
    services = fetch_service_map()
    if not services:
        log.error("error: could not fetch the service taxonomy (network/rate limit?)")
        return
    path = write_service_map(services)
    log.info(f"Fetched {len(services)} type->service mappings -> {path}")


def _run_standalone_command(args) -> Optional[int]:
    """Run a one-shot report command, or return ``None`` to generate the model."""
    if args.plan_keys or args.apply_keys:
        key_pass(
            args.service,
            apply=args.apply_keys,
            only_types=args.types,
            report_path=args.keys_report,
            dry_run=args.dry_run,
            metadata=args.metadata,
        )
        return 0
    if args.diff_metadata:
        compare_metadata(
            args.service,
            args.diff_metadata,
            args.diff_report,
            apply=args.apply_markers,
            only_types=args.types,
            dry_run=args.dry_run,
        )
        return 0
    if args.fetch_services:
        fetch_services()
        return 0
    if args.suggest_routing:
        suggest_routing(args.service)
        return 0
    if args.audit is not None:
        return audit_model(args.service, args.audit or None, args.audit_report, args.audit_fail)
    return None


#: Subcommand word -> the flag it stands for. ``generate`` is the default and adds none.
SUBCOMMANDS: dict[str, Optional[str]] = {
    "generate": None,
    "fetch": "--fetch",
    "routing": "--suggest-routing",
    "services": "--fetch-services",
    "keys": "--plan-keys",
    "verify": "--verify",
    "audit": "--audit",
}


def expand_subcommand(argv: Sequence[str]) -> list[str]:
    """Rewrite ``<subcommand> [args]`` to the equivalent flat flags (which keep working as given)."""
    args = list(argv)
    if args and args[0] in SUBCOMMANDS:
        flag = SUBCOMMANDS[args.pop(0)]
        if flag:
            # Last, so an optional-value flag such as --fetch never swallows the service name.
            args.append(flag)
    return args


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate entity model files from OData metadata")
    parser.add_argument(
        "service",
        nargs="?",
        default="graph",
        choices=service_names(),
        help="which model to generate (default: sharepoint)",
    )
    parser.add_argument("--dry-run", action="store_true", help="validate and report without writing files")
    parser.add_argument("--verbose", action="store_true", help="show debug-level generator messages")
    parser.add_argument(
        "--update-only",
        action="store_true",
        help="only update types that already exist in the model; never create new files",
    )
    parser.add_argument(
        "--type",
        dest="types",
        action="append",
        default=[],
        metavar="ODATA_TYPE",
        help="only process this OData type (e.g. SP.File); repeatable; with --apply-markers, only mark it",
    )
    parser.add_argument(
        "--metadata",
        metavar="PATH",
        help="read this metadata snapshot instead of the configured one (e.g. metadata/GraphBeta.xml)",
    )
    parser.add_argument("--report", dest="report_path", help="write a JSON run report to this path")
    parser.add_argument(
        "--force",
        action="store_true",
        help="ignore the up-to-date fast path and regenerate from scratch",
    )
    parser.add_argument(
        "--no-smoke",
        dest="smoke",
        action="store_false",
        help="skip importing the written modules after a successful run",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="run ruff and pyright on the output after writing (slow)",
    )
    parser.add_argument(
        "--fail-on-write",
        dest="fail_on_write",
        action="store_true",
        help="with --dry-run, exit non-zero when the run would create or update a file",
    )
    parser.add_argument(
        "--suggest-routing",
        action="store_true",
        help="print a proposed routing block for unrouted types and exit",
    )
    parser.add_argument(
        "--fetch-services",
        action="store_true",
        help="fetch the Graph docs service taxonomy (for --suggest-routing) and exit",
    )
    parser.add_argument(
        "--verify",
        nargs="?",
        const="",
        metavar="PACKAGE",
        help="check the rendered model's declarations and exit (default: office365)",
    )
    parser.add_argument(
        "--audit",
        nargs="?",
        const="",
        metavar="PACKAGE",
        help="measure the model against its service metadata and exit (default: the service's own package)",
    )
    parser.add_argument(
        "--audit-report",
        dest="audit_report",
        metavar="PATH",
        help="with --audit: write the findings to this JSON file",
    )
    parser.add_argument(
        "--audit-fail",
        dest="audit_fail",
        action="store_true",
        help="with --audit: exit non-zero when the model and the metadata disagree",
    )
    parser.add_argument(
        "--diff-metadata",
        dest="diff_metadata",
        metavar="PATH",
        help="compare the configured metadata with another snapshot (e.g. metadata/GraphBeta.xml) and exit",
    )
    parser.add_argument(
        "--diff-report",
        dest="diff_report",
        metavar="PATH",
        help="write the --diff-metadata comparison to this JSON file",
    )
    parser.add_argument(
        "--plan-keys",
        dest="plan_keys",
        action="store_true",
        help="print the @key(...) declarations the metadata justifies and exit",
    )
    parser.add_argument(
        "--apply-keys",
        dest="apply_keys",
        action="store_true",
        help="write the @key(...) declarations the metadata justifies into the model (with --dry-run: preview)",
    )
    parser.add_argument(
        "--keys-report",
        dest="keys_report",
        metavar="PATH",
        help="with --plan-keys/--apply-keys: write the plan to this JSON file",
    )
    parser.add_argument(
        "--apply-markers",
        dest="apply_markers",
        action="store_true",
        help="with --diff-metadata: write the justified @odata(beta=...) markers into the model",
    )
    parser.add_argument(
        "--fetch",
        dest="fetch",
        nargs="?",
        const="",
        metavar="PATH",
        help="download the service's metadata from the live endpoint (default: its snapshot under metadata/) and exit",
    )
    parser.add_argument(
        "--graph-version",
        dest="graph_version",
        default=None,
        help="with --fetch on graph: API version, e.g. v1.0 or beta",
    )
    args = parser.parse_args(expand_subcommand(sys.argv[1:] if argv is None else argv))
    configure_logging(args.verbose)
    try:
        if args.fetch is not None:
            from generator.metadata.fetch import fetch

            log.info(f"Wrote {fetch(args.service, args.graph_version, args.fetch or None)}")
            return 0
        if args.verify is not None:
            return verify_model(args.verify or None)
        handled = _run_standalone_command(args)
        if handled is not None:
            return handled
        if args.fail_on_write and not args.dry_run:
            raise ValidationError("--fail-on-write reports what a run would write, so it needs --dry-run")
        written = generate(
            args.service,
            dry_run=args.dry_run,
            update_only=args.update_only,
            only_types=args.types,
            report_path=args.report_path,
            metadata=args.metadata,
            # The gate asserts the tree against the snapshot, so it cannot trust the
            # manifest's "up to date": a stale manifest would pass it silently.
            force=args.force or args.fail_on_write,
            smoke=args.smoke,
            check=args.check,
        )
        if args.fail_on_write and written:
            raise ValidationError(
                f"{written} file(s) the {args.service} metadata declares are not in the tree; "
                "run the generator and commit the result"
            )
    except ValidationError as e:
        log.error(f"error: {e}")
        return 1
    except ConfigError as e:
        log.error(f"config error: {e}")
        return 1
    return 0
