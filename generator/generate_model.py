import json
import os
from configparser import ConfigParser
from pathlib import Path

from office365.runtime.odata.model import ODataModel
from office365.runtime.odata.v3.metadata_reader import ODataV3Reader
from office365.runtime.odata.v4.metadata_reader import ODataV4Reader

from generator.builders.type_builder import TypeBuilder
from generator.documentation.baseservice import BaseDocumentationService
from generator.documentation.graphdocsservice import GraphOpenService
from generator.documentation.sharepointdocsservice import SharePointService


def generate_files(model: ODataModel, options: dict, docs_service: BaseDocumentationService = None) -> None:
    metadata_path = options["metadatapath"]
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

        processed_count += 1
        print(f"[{processed_count}/{total_types}] Processing: {name}")

        try:
            type_schema = model.types[name]
            builder = TypeBuilder(type_schema, options, docs_service)
            builder.build()
            if builder.status == "created" or builder.status == "updated":
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


def generate_sharepoint_model(cp: ConfigParser) -> None:
    reader = ODataV3Reader(cp.get("sharepoint", "metadataPath"))
    # reader.format_file()
    model = reader.generate_model()
    docs_service = SharePointService()
    generate_files(model, dict(cp.items("sharepoint")), docs_service)


def generate_graph_model(cp: ConfigParser) -> None:
    reader = ODataV4Reader(cp.get("microsoftgraph", "metadataPath"))
    model = reader.generate_model()
    docs_service = GraphOpenService()
    generate_files(model, dict(cp.items("microsoftgraph")), docs_service)


if __name__ == "__main__":
    settings = ConfigParser()
    settings.read(Path(__file__).parent / "settings.cfg")
    generate_graph_model(settings)
    # generate_sharepoint_model(settings)
