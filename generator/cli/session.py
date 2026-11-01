"""Shared setup for CLI commands: service definition, options and metadata source."""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Optional

from generator.core.config import GeneratorOptions
from generator.core.services import ServiceDefinition, get_service
from generator.odata.model import ODataModel

#: Config/paths are resolved relative to this directory, not the CWD.
GENERATOR_DIR = Path(__file__).resolve().parent.parent


def resolve_path(path: str) -> Path:
    """A metadata path as given, or relative to the generator directory."""
    return Path(path) if Path(path).is_absolute() else GENERATOR_DIR / path


@dataclass(frozen=True)
class Session:
    """What every command needs: the service, its options, and where metadata is read from."""

    service: str
    definition: ServiceDefinition
    options: GeneratorOptions

    @classmethod
    def open(cls, service: str, *, dry_run: bool = False, metadata: Optional[str] = None) -> Session:
        options = GeneratorOptions.load(service, GENERATOR_DIR, dry_run=dry_run)
        if metadata:
            options = replace(options, metadata_path=str(resolve_path(metadata)))
        return cls(service, get_service(service), options)

    def read_model(self, metadata_path: Optional[str] = None) -> ODataModel:
        """The model of the configured snapshot, or of ``metadata_path`` when given."""
        return self.definition.reader(metadata_path or self.options.metadata_path).read()
