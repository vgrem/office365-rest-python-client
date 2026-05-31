import json
import os
from configparser import ConfigParser
from pathlib import Path
from typing import Dict, Optional

from office365.runtime.odata.model import ODataModel
from office365.runtime.odata.v3.metadata_reader import ODataV3Reader
from office365.runtime.odata.v4.metadata_reader import ODataV4Reader

from generator.builders.type import TypeBuilder
from generator.documentation.baseservice import BaseDocumentationService
from generator.documentation.graphdocsservice import GraphOpenService
from generator.documentation.sharepointdocsservice import SharePointService

KEY_ALIASES: Dict[str, str] = {
    "metadatapath": "metadata_path",
    "outputpath": "output_path",
    "templatepath": "template_path",
    "ignoredproperties": "ignored_properties",
    "includebasetypes": "include_base_types",
}


def _normalize_options(options: dict) -> dict:
    """Normalize config keys to modern names while accepting legacy keys."""
    normalized = {}
    for k, v in options.items():
        k_lower = k.lower()
        target = KEY_ALIASES.get(k_lower, k_lower)
        if target not in normalized:
            normalized[target] = v
    return normalized


def generate_files(model: ODataModel, options: dict, docs_service: Optional[BaseDocumentationService] = None) -> None:
    options = _normalize_options(options)
    metadata_path = options["metadata_path"]
    checkpoint_file = f".checkpoints/{os.path.basename(metadata_path)}.json"
    os.makedirs(".checkpoints", exist_ok=True)

    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r", encoding="utf-8") as f:
            processed_types = set(json.load(f))
        print(f"Resuming from checkpoint: {len(processed_types)} types already processed")
    else:
        processed_types = set()

    ignored_types = [t.strip() for t in options["ignoredtypes"].split(",")]
    exact_ignored = []
    prefix_ignored = []
    total_types = len(model.types)
    processed_count = len(processed_types)

    for ignored_type in ignored_types:
        if ignored_type.endswith(".*"):
            prefix_ignored.append(ignored_type[:-2])
        else:
            exact_ignored.append(ignored_type)

    for name in model.types:
        if name in processed_types:
            continue

        if name in exact_ignored:
            continue

        if any(name.startswith(prefix) for prefix in prefix_ignored):
            continue

        type_schema = model.types[name]

        include_base_types = options.get("include_base_types", options.get("includebasetypes", ""))
        if include_base_types:
            allowed = set(t.strip() for t in include_base_types.split(","))
            if type_schema.BaseTypeFullName not in allowed:
                processed_types.add(name)
                print(f"  Skipping {name} (BaseType={type_schema.BaseTypeFullName})")
                continue

        processed_count += 1
        print(f"[{processed_count}/{total_types}] Processing: {name}")

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

    if checkpoint_file and os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)


def _load_options(cp: ConfigParser, section: str) -> dict:
    """Load options for a section, including routing and key normalization."""
    options = dict(cp.items(section))
    if cp.has_section("routing"):
        for k, v in cp.items("routing"):
            options[f"routing_{k}"] = v
    return _normalize_options(options)


def generate_sharepoint_model(cp: ConfigParser) -> None:
    reader = ODataV3Reader(cp.get("sharepoint", "metadataPath"))
    # reader.format_file()
    model = reader.generate_model()
    docs_service = SharePointService()
    options = _load_options(cp, "sharepoint")
    generate_files(model, options, docs_service)


def generate_graph_model(cp: ConfigParser) -> None:
    reader = ODataV4Reader(cp.get("graph", "metadataPath"))
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
