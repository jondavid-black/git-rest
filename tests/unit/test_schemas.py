import pytest
from pydantic import ValidationError
from git_rest.schemas import RepoNameSchema, BranchNameSchema, FilePathSchema

def test_repo_name_schema_valid():
    s = RepoNameSchema(name="repo-1.2_3")
    assert s.name == "repo-1.2_3"

def test_repo_name_schema_invalid():
    with pytest.raises(ValidationError):
        RepoNameSchema(name="bad name!")

def test_branch_name_schema_valid():
    s = BranchNameSchema(name="feature/awesome")
    assert s.name == "feature/awesome"

def test_branch_name_schema_invalid():
    for bad in [".", "..", "/foo", "foo/", "foo//bar", "foo\\bar", "foo~bar", "foo^bar", "foo:bar", "foo?bar", "foo*bar", "foo[bar", "foo]bar", "foo@bar", "foo{bar", "foo}bar"]:
        with pytest.raises(ValidationError):
            BranchNameSchema(name=bad)

def test_file_path_schema_valid():
    s = FilePathSchema(path="foo/bar.txt")
    assert s.path == "foo/bar.txt"

def test_file_path_schema_invalid():
    for bad in ["/abs/path", "foo/../bar", "../bar", "foo/../../bar"]:
        with pytest.raises(ValidationError):
            FilePathSchema(path=bad)
