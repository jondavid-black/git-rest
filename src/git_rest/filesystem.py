import os



import threading
import fcntl

class FileSystemIsolation:
    """
    Enforces user namespace isolation for all file operations.
    All paths are resolved relative to the user's base directory.
    No cross-user access is possible by construction.
    Adds concurrency-safe (thread/process) locking for all repo/branch/file actions.
    """
    _global_lock = threading.Lock()  # fallback for in-memory lock

    def __init__(self, base_dir: str | None = None):
        # base_dir should be user-specific (e.g., /tmp/git-rest/<user_id>)
        self.base_dir = base_dir or os.environ.get("GIT_REST_WORKDIR", "/tmp/git-rest")
        self.base_dir = os.path.abspath(self.base_dir)
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir, exist_ok=True)
        self._lockfile_path = os.path.join(self.base_dir, ".fslock")
        # Ensure lockfile exists
        with open(self._lockfile_path, "a") as _:
            pass

    def safe_join(self, *paths) -> str:
        # Join and resolve to absolute path within the user's namespace
        joined = os.path.abspath(os.path.join(self.base_dir, *paths))
        # Enforce: only allow access within the user's base_dir
        if not (joined == self.base_dir or joined.startswith(self.base_dir + os.sep)):
            raise ValueError(
                "Path traversal detected or path outside allowed user directory"
            )
        return joined

    def _acquire_lock(self, blocking=True):
        """
        Acquire a file-based lock for this user's namespace.
        Returns a context manager that holds the lock.
        """
        class LockContext:
            def __init__(self, lockfile_path, blocking):
                self.lockfile_path = lockfile_path
                self.blocking = blocking
                self.lockfile = None
            def __enter__(self):
                self.lockfile = open(self.lockfile_path, "r+")
                if self.blocking:
                    fcntl.flock(self.lockfile, fcntl.LOCK_EX)
                else:
                    fcntl.flock(self.lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self.lockfile
            def __exit__(self, exc_type, exc_val, exc_tb):
                fcntl.flock(self.lockfile, fcntl.LOCK_UN)
                self.lockfile.close()
        return LockContext(self._lockfile_path, blocking)

    def is_safe_path(self, path: str) -> bool:
        # Check if the given path is within the user's namespace
        abs_path = os.path.abspath(os.path.join(self.base_dir, path))
        return abs_path.startswith(self.base_dir + os.sep)


    def list_dir(self, rel_path: str = ""):
        with self._acquire_lock():
            dir_path = self.safe_join(rel_path)
            if not os.path.isdir(dir_path):
                raise FileNotFoundError(f"Directory not found: {rel_path}")
            return os.listdir(dir_path)


    def file_exists(self, rel_path: str) -> bool:
        with self._acquire_lock():
            return os.path.isfile(self.safe_join(rel_path))


    def dir_exists(self, rel_path: str) -> bool:
        with self._acquire_lock():
            return os.path.isdir(self.safe_join(rel_path))
