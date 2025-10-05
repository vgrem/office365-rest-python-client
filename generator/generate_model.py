from configparser import ConfigParser
from pathlib import Path

from generator.builders.type_builder import TypeBuilder
from office365.runtime.odata.model import ODataModel
from office365.runtime.odata.v3.metadata_reader import ODataV3Reader
from office365.runtime.odata.v4.metadata_reader import ODataV4Reader


def generate_files(model: ODataModel, options: dict) -> None:
    ignored_types = [t.strip() for t in options["ignoredtypes"].split(",")]
    exact_ignored = []
    prefix_ignored = []

    for ignored_type in ignored_types:
        if ignored_type.endswith(".*"):
            prefix_ignored.append(ignored_type[:-2])
        else:
            exact_ignored.append(ignored_type)

    for name in model.types:
        if name in exact_ignored:
            continue

        if any(name.startswith(prefix) for prefix in prefix_ignored):
            continue

        type_schema = model.types[name]
        builder = TypeBuilder(type_schema, options)
        builder.build()
        if builder.status == "created" or builder.status == "updated":
            builder.save()


def generate_sharepoint_model(cp: ConfigParser) -> None:
    reader = ODataV3Reader(cp.get("sharepoint", "metadataPath"))
    # reader.format_file()
    model = reader.generate_model()
    generate_files(model, dict(cp.items("sharepoint")))


def generate_graph_model(cp: ConfigParser) -> None:
    reader = ODataV4Reader(cp.get("microsoftgraph", "metadataPath"))
    model = reader.generate_model()
    generate_files(model, dict(cp.items("microsoftgraph")))


if __name__ == "__main__":
    settings = ConfigParser()
    settings.read(Path(__file__).parent / "settings.cfg")
    generate_graph_model(settings)
    #generate_sharepoint_model(settings)
