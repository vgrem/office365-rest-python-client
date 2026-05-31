import json
import os
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

from office365.runtime.odata.model import ODataModel
from office365.runtime.odata.v3.metadata_reader import ODataV3Reader
from office365.runtime.odata.v4.metadata_reader import ODataV4Reader

from generator.builders.type import TypeBuilder
from generator.documentation.baseservice import BaseDocumentationService
from generator.documentation.graphdocsservice import GraphOpenService
from generator.documentation.sharepointdocsservice import SharePointService


def _should_skip(
    name: str, type_schema, processed_types: set, exact_ignored: list, prefix_ignored: list, options: dict
) -> tuple[bool, bool]:
    """Check skip conditions. Returns (should_skip, raised_error)."""
    if name in processed_types:
        return True, False

    pending_skip_type = options.get("include_base_types", "")
    if pending_skip_type:
        allowed = set(t.strip() for t in pending_skip_type.split(","))
        if type_schema.BaseTypeFullName not in allowed:
            processed_types.add(name)
            print(f"  Skipping {name} (BaseType={type_schema.BaseTypeFullName})")
            return True, False

    if name in exact_ignored:
        return True, False

    if any(name.startswith(p) for p in prefix_ignored):
        return True, False

    return False, False


def _process_type(
    name: str, type_schema, checkpoint_file: str, options: dict, docs_service, processed_types: set
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
    checkpoint_file = f".checkpoints/{os.path.basename(metadata_path)}.json"
    os.makedirs(".checkpoints", exist_ok=True)

    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r", encoding="utf-8") as f:
            processed_types = set(json.load(f))
        print(f"Resuming from checkpoint: {len(processed_types)} types already processed")
    else:
        processed_types = set()

    ignored_types_raw = options.get("filters_ignored_types", "")
    ignored_types = [t.strip() for t in ignored_types_raw.replace("\n", ",").split(",") if t.strip()]
    exact_ignored = []
    prefix_ignored = []

    for ignored_type in ignored_types:
        if ignored_type.endswith(".*"):
            prefix_ignored.append(ignored_type[:-2])
        else:
            exact_ignored.append(ignored_type)

    start_at = options.get("start_at", "")
    started = not start_at
    if start_at and not any(n.startswith(start_at) for n in model.types):
        print(f"  Warning: start_at '{start_at}' does not match any types, proceeding from beginning")

    total_types = len(model.types)
    processed_count = len(processed_types)

    for name in model.types:
        if name in processed_types:
            continue

        if not started:
            if name.startswith(start_at):
                started = True
            else:
                print(f"  Skipping {name} (start_at={start_at})")
                processed_types.add(name)
                continue

        type_schema = model.types[name]
        skip, _ = _should_skip(name, type_schema, processed_types, exact_ignored, prefix_ignored, options)
        if skip:
            continue

        processed_count += 1
        print(f"[{processed_count}/{total_types}] Processing: {name}")
        _process_type(name, type_schema, checkpoint_file, options, docs_service, processed_types)

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
    return options


def generate_sharepoint_model(cp: ConfigParser) -> None:
    reader = ODataV3Reader(cp.get("sharepoint", "metadata_path"))
    # reader.format_file()
    model = reader.generate_model()
    docs_service = SharePointService()
    options = _load_options(cp, "sharepoint")
    generate_files(model, options, docs_service)


def generate_graph_model(cp: ConfigParser) -> None:
    reader = ODataV4Reader(cp.get("graph", "metadata_path"))
    model = reader.generate_model()
    docs_service = GraphOpenService()
    options = _load_options(cp, "graph")
    generate_files(model, options, docs_service)


if __name__ == "__main__":
    graph_cfg = ConfigParser()
    graph_cfg.read(Path(__file__).parent / "settings.graph.cfg")
    generate_graph_model(graph_cfg)

    # sharepoint_cfg = ConfigParser()
    # sharepoint_cfg.read(Path(__file__).parent / "settings.sharepoint.cfg")
    # generate_sharepoint_model(sharepoint_cfg)
