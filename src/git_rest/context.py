
import threading
import logging
import os

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


def configure_environment():
    """
    Configure environment variables and logging for the application.
    """
    # Set up logging
    log_level = os.environ.get("GIT_REST_LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    logging.getLogger("git_rest").info(f"Logging initialized at {log_level} level.")

    # Set up workdir
    workdir = os.environ.get("GIT_REST_WORKDIR", "/tmp/git-rest")
    if not os.path.exists(workdir):
        os.makedirs(workdir, exist_ok=True)
    logging.getLogger("git_rest").info(f"Workdir set to {workdir}")
