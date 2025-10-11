import logging

from git_rest.context import RepoContext, configure_environment


def test_repo_context_set_get_clear():
    RepoContext.set_current_repo("repo1")
    assert RepoContext.get_current_repo() == "repo1"
    RepoContext.clear_current_repo()
    assert RepoContext.get_current_repo() is None


def test_configure_environment_sets_log_and_workdir(tmp_path, monkeypatch, caplog):
    monkeypatch.setenv("GIT_REST_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("GIT_REST_WORKDIR", str(tmp_path))
    caplog.set_level(logging.DEBUG)
    configure_environment()
    assert tmp_path.exists()
    # Check log output
    found_log = any(
        "Logging initialized at DEBUG level." in r.message for r in caplog.records
    )
    found_workdir = any(
        f"Workdir set to {tmp_path}" in r.message for r in caplog.records
    )
    assert found_log
    assert found_workdir
