from pydantic import BaseModel, Field, validator
import re

class RepoNameSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

    @validator('name')
    def valid_repo_name(cls, v):
        if not re.match(r'^[\w.-]+$', v):
            raise ValueError('Repository name must be alphanumeric, dash, dot, or underscore')
        return v

class BranchNameSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

    @validator('name')
    def valid_branch_name(cls, v):
        # Git branch name rules (simplified)
        if v in {'.', '..'} or v.startswith('/') or v.endswith('/') or '//' in v or '\\' in v:
            raise ValueError('Invalid branch name')
        if not re.match(r'^[^~^:?*\[\]@{}\\]+$', v):
            raise ValueError('Branch name contains invalid characters')
        return v

class FilePathSchema(BaseModel):
    path: str = Field(..., min_length=1, max_length=4096)

    @validator('path')
    def valid_file_path(cls, v):
        if v.startswith('/') or '..' in v.split('/'):
            raise ValueError('File path must be relative and not contain path traversal')
        return v
