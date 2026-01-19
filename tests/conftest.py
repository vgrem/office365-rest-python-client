import unittest
from typing import Any

import pytest

from tests.graph_case import GraphTestCase
from tests.sharepoint.sharepoint_case import SPTestCase


def pytest_addoption(parser: pytest.Parser) -> None:
    """Support command line marks."""
    parser.addoption("--offline", action="store_true", help="exclude all Graph tests")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Skip tests based on command line options."""
    if not config.getoption("--offline"):
        return
    skip_mrk = pytest.mark.skip(reason="--offline exclude all Graph tests")
    for item in items:
        if issubclass(item.cls, (GraphTestCase, SPTestCase)):  # type: ignore[attr-defined]
            item.add_marker(skip_mrk)
