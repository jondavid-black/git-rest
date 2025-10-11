import logging
from functools import wraps

logger = logging.getLogger("git_rest.audit")

# Simple audit log decorator for repository operations
def audit_repo_action(action):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = getattr(getattr(args[0], 'user', None), 'username', 'anonymous') if args else 'anonymous'
            logger.info(f"[AUDIT] user={user} action={action} args={args} kwargs={kwargs}")
            return f(*args, **kwargs)
        return wrapper
    return decorator
