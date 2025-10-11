from datetime import datetime

from pydantic import BaseModel


class Remote(BaseModel):
    name: str
    url: str


class Branch(BaseModel):
    name: str
    is_current: bool = False


class Commit(BaseModel):
    hash: str
    author: str
    date: datetime
    message: str
    parent_hashes: list[str] = []


class FileEntry(BaseModel):
    path: str
    type: str  # file, dir, symlink
    size: int
    last_modified: datetime


class RepoStatus(BaseModel):
    staged: list[FileEntry] = []
    unstaged: list[FileEntry] = []
    untracked: list[FileEntry] = []


class Repository(BaseModel):
    id: str
    name: str
    path: str
    remotes: list[Remote] = []
    branches: list[Branch] = []
    current_branch: str | None = None
    status: RepoStatus | None = None
