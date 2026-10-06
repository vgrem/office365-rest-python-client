"""Offline tests for the response-byte normalizers.

``ClientResult.to_bytes`` and ``Report.to_bytes`` back the report-download
examples, which previously inlined ``isinstance(value, bytes)`` checks.
"""

from __future__ import annotations

from office365.reports.report import Report
from office365.runtime.client_result import ClientResult


def test_client_result_to_bytes_from_raw_bytes():
    assert ClientResult(None, b"abc").to_bytes() == b"abc"


def test_client_result_to_bytes_from_bytearray():
    assert ClientResult(None, bytearray(b"abc")).to_bytes() == b"abc"


def test_client_result_to_bytes_from_str():
    assert ClientResult(None, "abc").to_bytes() == b"abc"


def test_client_result_to_bytes_from_report():
    assert ClientResult(None, Report(content=b"csv,bytes")).to_bytes() == b"csv,bytes"


def test_client_result_to_bytes_from_object_with_str_content():
    class _Wrapper:
        content = "text"

    assert ClientResult(None, _Wrapper()).to_bytes() == b"text"


def test_client_result_to_bytes_when_empty():
    assert ClientResult(None).to_bytes() == b""
    assert ClientResult(None, Report()).to_bytes() == b""


def test_report_to_bytes():
    assert Report(content=b"x").to_bytes() == b"x"
    assert Report().to_bytes() == b""
