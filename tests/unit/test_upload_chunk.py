"""Upload-session chunk arithmetic has one home, and every session reads it.

A Graph upload session rejects any byte range that is not a positive multiple of
320 KiB, so a number hard-coded in one method is a defect the service finds at run
time. Three sessions used to carry their own: ``1000000`` for a mail attachment,
``1000000 * 3`` for a large one, and 4 MiB for a To Do attachment. The rule now lives
in :mod:`office365.runtime.transfer`; these tests pin the rule and pin every session
to it, so a fourth upload path cannot quietly introduce a fourth number.
"""

import importlib
import inspect

import pytest
from office365.onedrive.driveitems.driveItem import DriveItem
from office365.outlook.mail.attachments.collection import AttachmentCollection
from office365.runtime.transfer import (
    INLINE_ATTACHMENT_MAX,
    UPLOAD_CHUNK_DEFAULT,
    UPLOAD_CHUNK_MAX,
    UPLOAD_CHUNK_UNIT,
    check_chunk_size,
)
from office365.todo.attachments.session import AttachmentSession
from office365.todo.tasks.task import TodoTask

UPLOADERS = (
    DriveItem.resumable_upload,
    AttachmentCollection.resumable_upload,
    AttachmentSession.upload,
    TodoTask.upload_attachment,
)


def test_a_chunk_is_a_positive_multiple_of_the_unit_and_no_more_than_the_ceiling():
    for good in (UPLOAD_CHUNK_UNIT, UPLOAD_CHUNK_DEFAULT, UPLOAD_CHUNK_MAX):
        check_chunk_size(good)  # returns None, i.e. accepted

    for bad in (0, -UPLOAD_CHUNK_UNIT, UPLOAD_CHUNK_UNIT + 1, UPLOAD_CHUNK_MAX + UPLOAD_CHUNK_UNIT):
        with pytest.raises(ValueError, match="multiple of 320 KiB|at most 60 MiB"):
            check_chunk_size(bad)


def test_the_numbers_three_sessions_used_to_carry_are_refused():
    # 1 MB, 3 MB and 4 MB are plausible-looking and each is off by a fraction of a unit,
    # which is exactly why the service rejected them and why the check must be arithmetic.
    for wrong in (1_000_000, 3_000_000, 4 * 1024 * 1024):
        with pytest.raises(ValueError, match="multiple of 320 KiB"):
            check_chunk_size(wrong)


@pytest.mark.parametrize(
    "module_name",
    ("office365.outlook.mail.messages.message", "office365.todo.tasks.task"),
)
def test_the_inline_attachment_threshold_is_declared_once(module_name):
    # Both attachment collections dispatch at the same published bound; a re-declared
    # 3 MiB literal in either module would be a second home for one policy number.
    assert importlib.import_module(module_name).INLINE_ATTACHMENT_MAX is INLINE_ATTACHMENT_MAX


@pytest.mark.parametrize("upload_method", UPLOADERS, ids=lambda m: m.__qualname__)
def test_every_upload_session_defaults_to_a_valid_chunk(upload_method):
    default = inspect.signature(upload_method).parameters["chunk_size"].default
    assert default == UPLOAD_CHUNK_DEFAULT
    check_chunk_size(default)
