import pytest
import tempfile
import os
import json
from git_rest.audit import write_audit_log, audit_repo_action

def test_write_audit_log_creates_file_and_entry(tmp_path, monkeypatch):
    monkeypatch.setenv("GIT_REST_AUDIT_LOG_DIR", str(tmp_path))
    user_id = "user1"
    action_type = "test_action"
    target_resource = "repo:foo"
    outcome = "success"
    extra = {"foo": "bar"}
    write_audit_log(user_id, action_type, target_resource, outcome, extra)
    log_file = tmp_path / f"{user_id}.log"
    assert log_file.exists()
    with open(log_file) as f:
        line = f.readline()
        entry = json.loads(line)
        assert entry["user_id"] == user_id
        assert entry["action_type"] == action_type
        assert entry["target_resource"] == target_resource
        assert entry["outcome"] == outcome
        assert entry["foo"] == "bar"

def test_audit_repo_action_decorator_success(monkeypatch, tmp_path):
    monkeypatch.setenv("GIT_REST_AUDIT_LOG_DIR", str(tmp_path))
    from flask import Flask
    app = Flask(__name__)
    calls = {}
    @audit_repo_action("myaction")
    def f(repo_id):
        calls["called"] = True
        return "ok", 200
    with app.test_request_context():
        result = f("repo42")
    assert result == ("ok", 200)
    log_file = tmp_path / "anonymous.log"
    assert log_file.exists()
    with open(log_file) as f:
        entry = json.loads(f.readline())
        assert entry["action_type"] == "myaction"
        assert entry["outcome"] == "success"
        assert entry["target_resource"] == "repo:repo42"
        assert calls["called"]

def test_audit_repo_action_decorator_failure(monkeypatch, tmp_path):
    monkeypatch.setenv("GIT_REST_AUDIT_LOG_DIR", str(tmp_path))
    from flask import Flask
    app = Flask(__name__)
    @audit_repo_action("failaction")
    def f(repo_id):
        raise ValueError("fail")
    with app.test_request_context():
        with pytest.raises(ValueError):
            f("repo99")
    log_file = tmp_path / "anonymous.log"
    assert log_file.exists()
    with open(log_file) as f:
        entry = json.loads(f.readline())
        assert entry["action_type"] == "failaction"
        assert entry["outcome"].startswith("failure:")
        assert entry["target_resource"] == "repo:repo99"
        assert "error" in entry
