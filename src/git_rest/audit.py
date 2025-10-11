import logging
import os
from datetime import datetime
from functools import wraps

from flask import request

logger = logging.getLogger("git_rest.audit")


def write_audit_log(user_id, action_type, target_resource, outcome, extra=None):
    """
    Write an audit log entry for the given user.
    Log fields: user_id, action_type, target_resource, timestamp, outcome, extra
    """
    log_dir = os.environ.get("GIT_REST_AUDIT_LOG_DIR", "/tmp/git-rest/audit-logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{user_id}.log")
    from datetime import datetime, UTC
    timestamp = datetime.now(UTC).isoformat()
    entry = {
        "user_id": user_id,
        "action_type": action_type,
        "target_resource": target_resource,
        "timestamp": timestamp,
        "outcome": outcome,
    }
    if extra:
        entry.update(extra)
    # Write as a single line JSON for easy parsing
    import json

    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")
    logger.info(f"[AUDIT] {entry}")


def audit_repo_action(action):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = getattr(getattr(request, "user", None), "username", "anonymous")
            repo_id = kwargs.get("repo_id") or (args[0] if args else None)
            file_path = (
                kwargs.get("file_path")
                if "file_path" in kwargs
                else (args[1] if len(args) > 1 else None)
            )
            target_resource = f"repo:{repo_id}"
            if file_path:
                target_resource += f"/file:{file_path}"
            try:
                result = f(*args, **kwargs)
                # Determine outcome from response (Flask response tuple or object)
                status = None
                if isinstance(result, tuple):
                    status = result[1]
                elif hasattr(result, "status_code"):
                    status = result.status_code
                outcome = (
                    "success"
                    if (status is None or (200 <= status < 400))
                    else f"failure:{status}"
                )
            except Exception as e:
                outcome = f"failure:{type(e).__name__}"
                write_audit_log(
                    user, action, target_resource, outcome, extra={"error": str(e)}
                )
                raise
            write_audit_log(user, action, target_resource, outcome)
            return result

        return wrapper

    return decorator
