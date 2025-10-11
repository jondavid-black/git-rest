from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

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
    parent_hashes: List[str] = []

class FileEntry(BaseModel):
    path: str
    type: str  # file, dir, symlink
    size: int
    last_modified: datetime

class RepoStatus(BaseModel):
    staged: List[FileEntry] = []
    unstaged: List[FileEntry] = []
    untracked: List[FileEntry] = []

class Repository(BaseModel):
    id: str
    name: str
    path: str
    remotes: List[Remote] = []
    branches: List[Branch] = []
    current_branch: Optional[str] = None
    status: Optional[RepoStatus] = None
