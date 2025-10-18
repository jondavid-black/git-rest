from datetime import UTC, datetime
from enum import Enum


class FileType(str, Enum):
    TEXT = "text"
    BINARY = "binary"


class FileStatus(str, Enum):
    STAGED = "staged"
    UNSTAGED = "unstaged"


class File:
    def __init__(
        self,
        path: str,
        type: FileType,
        content: str,
        status: FileStatus = FileStatus.UNSTAGED,
        last_updated: datetime | None = None,
        locked: bool = False,
    ):
        self.path = path
        self.type = type
        self.content = content
        self.status = status
        self.last_updated = last_updated or datetime.now(UTC)
        self.locked = locked

    def stage(self):
        self.status = FileStatus.STAGED
        self.last_updated = datetime.now(UTC)

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False
