"""Command line entry point for the model generator."""

from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path
from typing import Optional, Sequence

from generator.beta_markers import compare_markers, plan_markers, read_declared_markers, read_declared_versions
from generator.beta_markers import write_report as write_marker_report
from generator.builders.resolution import TypeRegistry
from generator.config import ConfigError, GeneratorOptions
from generator.documentation.subservices import fetch_service_map, load_service_map, write_service_map
from generator.filters import TypeFilter
from generator.manifest import Manifest, is_up_to_date
from generator.metadata_diff import diff_metadata, write_report
from generator.odata.reader import ODataReader
from generator.pipeline import GeneratorPipeline
from generator.routing import Router, render_suggestions
from generator.services import get_service, service_names
from generator.validation import ValidationError

#: Config/paths are resolved relative to this directory, not the CWD.
GENERATOR_DIR = Path(__file__).parent


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
) -> None:
    """Read the service metadata and generate/update the corresponding model files.

    ``metadata`` reads a different snapshot than the configured one -- the preview CSDL
    -- while the routing, filters and output tree stay exactly what the service config
    says. That is what makes one model possible: the tree is the union, the snapshot
    decides what is new, and the marker pass records which root declares what.
    """
    definition = get_service(service)
    options = GeneratorOptions.load(service, GENERATOR_DIR, dry_run=dry_run)
    if metadata:
        source = Path(metadata) if Path(metadata).is_absolute() else GENERATOR_DIR / metadata
        options = replace(options, metadata_path=str(source))
    if is_up_to_date(
        options,
        Manifest.load(options.metadata_path, GENERATOR_DIR),
        force=force,
        targeted=bool(only_types or report_path),
    ):
        print("Model is up to date (metadata and config unchanged); nothing to do.")
        return
    reader: ODataReader = definition.reader(options.metadata_path)
    documentation = definition.documentation() if definition.documentation else None
    GeneratorPipeline(
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
    definition = get_service(service)
    options = GeneratorOptions.load(service, GENERATOR_DIR)
    model = definition.reader(options.metadata_path).read()
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
    definition = get_service(service)
    options = GeneratorOptions.load(service, GENERATOR_DIR)
    other = Path(other_path) if Path(other_path).is_absolute() else GENERATOR_DIR / other_path
    base = definition.reader(options.metadata_path).read()
    target = definition.reader(str(other)).read()
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
        print(f"\nFull report written to {report_path}")
    if apply:
        _apply_marker_pass(options, plan.restricted(only_types) if only_types else plan, dry_run=dry_run)


def _apply_marker_pass(options: GeneratorOptions, plan, *, dry_run: bool) -> None:
    """Write the markers the plan justifies into the model, and say what it wrote."""
    from generator.marker_apply import TypeFiles, apply_markers

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


def _marker_report_path(report_path: str) -> str:
    """``delta.json`` -> ``beta_markers.json``, next to it."""
    path = Path(report_path)
    return str(path.with_name("beta_markers" + path.suffix))


def report_duplicates(service: str) -> None:
    """Print OData names claimed by more than one module (one shadows another)."""
    options = GeneratorOptions.load(service, GENERATOR_DIR)
    registry = TypeRegistry(options.modules.split(","), namespace=options.namespace)
    duplicates = registry.duplicate_types()
    if not duplicates:
        print("No duplicate OData names found.")
        return
    print(f"{len(duplicates)} duplicate OData name(s):")
    for name, modules in sorted(duplicates.items()):
        chosen = registry.strict_module_for(name) or registry.module_for(name)
        print(f"  {name}")
        for module in modules:
            marker = "  <- used" if module == chosen else ""
            print(f"    {module}{marker}")


def fetch_services() -> None:
    """Fetch the Graph docs service taxonomy and cache it for --suggest-routing."""
    services = fetch_service_map()
    if not services:
        print("error: could not fetch the service taxonomy (network/rate limit?)")
        return
    path = write_service_map(services)
    print(f"Fetched {len(services)} type->service mappings -> {path}")


def _run_standalone_command(args) -> Optional[int]:
    """Run a one-shot report command, or return ``None`` to generate the model."""
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
    if args.report_duplicates:
        report_duplicates(args.service)
        return 0
    return None


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate entity model files from OData metadata")
    parser.add_argument(
        "service",
        nargs="?",
        default="sharepoint",
        choices=service_names(),
        help="which model to generate (default: sharepoint)",
    )
    parser.add_argument("--dry-run", action="store_true", help="validate and report without writing files")
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
        "--report-duplicates",
        action="store_true",
        help="print OData names claimed by more than one module and exit",
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
        "--apply-markers",
        dest="apply_markers",
        action="store_true",
        help="with --diff-metadata: write the justified @odata(beta=...) markers into the model",
    )
    args = parser.parse_args(argv)
    handled = _run_standalone_command(args)
    if handled is not None:
        return handled
    try:
        generate(
            args.service,
            dry_run=args.dry_run,
            update_only=args.update_only,
            only_types=args.types,
            report_path=args.report_path,
            metadata=args.metadata,
            force=args.force,
            smoke=args.smoke,
            check=args.check,
        )
    except ValidationError as e:
        print(f"error: {e}")
        return 1
    except ConfigError as e:
        print(f"config error: {e}")
        return 1
    return 0
