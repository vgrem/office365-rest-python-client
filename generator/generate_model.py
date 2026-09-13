from __future__ import annotations

import argparse
import json
import os
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

from generator.builders.type import TypeBuilder
from generator.documentation.baseservice import BaseDocumentationService
from generator.documentation.graphdocsservice import GraphOpenService
from generator.documentation.sharepointdocsservice import SharePointService
from generator.odata.model import ODataModel
from generator.odata.reader import ODataReader
from generator.odata.type_information import TypeInformation
from generator.odata.v3.metadata_reader import ODataV3Reader
from generator.odata.v4.metadata_reader import ODataV4Reader

_GENERATOR_DIR = Path(__file__).parent

_SERVICES = {
    "sharepoint": (ODataV3Reader, SharePointService),
    "graph": (ODataV4Reader, GraphOpenService),
}


def _resolve_path(value: str) -> str:
    """Resolve a config path relative to the generator directory (not the CWD)."""
    if os.path.isabs(value):
        return value
    return str((_GENERATOR_DIR / value).resolve())


def _parse_list(raw: str) -> list[str]:
    """Splits a comma/newline separated config value into stripped items."""
    return [item.strip() for item in raw.replace("\n", ",").split(",") if item.strip()]


def _split_ignored(raw: str) -> tuple[list[str], list[str]]:
    """Splits ignored type patterns into exact names and ``prefix*`` patterns."""
    exact: list[str] = []
    prefix: list[str] = []
    for pattern in _parse_list(raw):
        if pattern.endswith("*"):
            prefix.append(pattern[:-1])
        else:
            exact.append(pattern)
    return exact, prefix


def _should_skip(
    name: str,
    type_schema: TypeInformation,
    processed_types: set,
    exact_ignored: list,
    prefix_ignored: list,
    allowed_base_types: set,
) -> bool:
    """Check whether a type should be skipped."""
    if name in processed_types:
        return True
    if allowed_base_types and type_schema.BaseTypeFullName not in allowed_base_types:
        processed_types.add(name)
        print(f"  Skipping {name} (BaseType={type_schema.BaseTypeFullName})")
        return True
    if name in exact_ignored or any(name.startswith(p) for p in prefix_ignored):
        return True
    return False


def _process_type(
    name: str, type_schema: TypeInformation, checkpoint_file: str, options: dict, docs_service, processed_types: set
) -> None:
    """Build, save and checkpoint a single type."""
    try:
        builder = TypeBuilder(type_schema, options, docs_service)
        builder.build()
        if builder.status in {"created", "updated"}:
            builder.save()

        processed_types.add(name)
        with open(checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(list(processed_types), f)

    except Exception as e:
        print(f"Failed on {name}: {e}")
        print(f"Checkpoint saved. Resume will skip {len(processed_types)} processed types")
        raise


def generate_files(model: ODataModel, options: dict, docs_service: Optional[BaseDocumentationService] = None) -> None:
    metadata_path = options["metadata_path"]
    checkpoint_dir = _GENERATOR_DIR / ".checkpoints"
    checkpoint_file = checkpoint_dir / f"{os.path.basename(metadata_path)}.json"
    checkpoint_dir.mkdir(exist_ok=True)

    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r", encoding="utf-8") as f:
            processed_types = set(json.load(f))
        print(f"Resuming from checkpoint: {len(processed_types)} types already processed")
    else:
        processed_types = set()

    options = {**options, "ignored_properties": _parse_list(options.get("filters_ignored_properties", ""))}
    exact_ignored, prefix_ignored = _split_ignored(options.get("filters_ignored_types", ""))
    allowed_base_types = set(_parse_list(options.get("include_base_types", "")))

    start_at = options.get("start_at", "").strip()
    total_types = len(model.types)
    processed_count = len(processed_types)

    if start_at and start_at.isdigit():
        skip_count = int(start_at)
        if skip_count > 0:
            for i, name in enumerate(model.types):
                if i >= skip_count:
                    break
                processed_types.add(name)
            print(f"  Skipping first {skip_count} types (start_at={start_at})")

    for name in model.types:
        if name in processed_types:
            continue

        if start_at and not start_at.isdigit():
            if name.startswith(start_at):
                start_at = ""
            else:
                print(f"  Skipping {name} (start_at={start_at})")
                processed_types.add(name)
                continue

        type_schema = model.types[name]
        skip = _should_skip(name, type_schema, processed_types, exact_ignored, prefix_ignored, allowed_base_types)
        if skip:
            continue

        processed_count += 1
        print(f"[{processed_count}/{total_types}] Processing: {name}")
        _process_type(name, type_schema, str(checkpoint_file), options, docs_service, processed_types)

    if checkpoint_file and os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)


def _load_options(cp: ConfigParser, section: str) -> dict:
    """Load options by merging [section] + [filters] + [modules] + [routing]."""
    options = dict(cp.items(section))
    for sub in ("filters", "modules", "routing"):
        if cp.has_section(sub):
            for k, v in cp.items(sub):
                options[f"{sub}_{k}"] = v
    if cp.has_section("modules"):
        modules_list = [v for k, v in cp.items("modules")]
        options["modules"] = ",".join(modules_list)
    for key in ("metadata_path", "output_path", "template_path"):
        if options.get(key):
            options[key] = _resolve_path(options[key])
    return options


def generate(service: str) -> None:
    """Reads the service metadata and generates/updates the corresponding model files."""
    cfg = ConfigParser()
    cfg.read(_GENERATOR_DIR / f"settings.{service}.cfg")
    reader_cls, docs_cls = _SERVICES[service]
    options = _load_options(cfg, service)
    reader: ODataReader = reader_cls(options["metadata_path"])
    generate_files(reader.read(), options, docs_cls())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate entity model files from OData metadata")
    parser.add_argument(
        "service",
        nargs="?",
        default="sharepoint",
        choices=sorted(_SERVICES),
        help="which model to generate (default: sharepoint)",
    )
    args = parser.parse_args()
    generate(args.service)
