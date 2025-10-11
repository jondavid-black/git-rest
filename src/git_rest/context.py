import threading

class RepoContext:
    """
    Thread-local context for the currently selected repository per user/session.
    In production, this should be tied to user/session, not just thread.
    """
    _local = threading.local()

    @classmethod
    def set_current_repo(cls, repo_id: str):
        cls._local.current_repo = repo_id

    @classmethod
    def get_current_repo(cls) -> str:
        return getattr(cls._local, "current_repo", None)

    @classmethod
    def clear_current_repo(cls):
        if hasattr(cls._local, "current_repo"):
            del cls._local.current_repo
