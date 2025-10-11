import logging
from functools import wraps

from flask import request

logger = logging.getLogger("git_rest.audit")


# Simple audit log decorator for repository operations
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
            logger.info(
                f"[AUDIT] user={user} action={action} repo_id={repo_id} file_path={file_path} args={args} kwargs={kwargs}"
            )
            return f(*args, **kwargs)

        return wrapper

    return decorator
