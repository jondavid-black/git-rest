from threading import Lock

from git_rest.models.file import File


class FileLockManager:
    """Manages file-level locks for sequential updates."""

    def __init__(self):
        self._locks: dict[str, Lock] = {}

    def acquire(self, file_path: str, timeout: float | None = None) -> bool:
        if file_path not in self._locks:
            self._locks[file_path] = Lock()
        return self._locks[file_path].acquire(timeout=timeout)

    def release(self, file_path: str):
        if file_path in self._locks:
            self._locks[file_path].release()


class FileService:
    """Service for file operations, including locking and sequential updates."""

    def __init__(self, lock_manager: FileLockManager | None = None):
        self.lock_manager = lock_manager or FileLockManager()

    def update_file(self, file: File, new_content: str, timeout: float = 5.0) -> bool:
        # Sequential file-level locking
        acquired = self.lock_manager.acquire(file.path, timeout=timeout)
        if not acquired:
            return False  # Could not acquire lock (timeout)
        try:
            file.content = new_content
            file.stage()
            return True
        finally:
            self.lock_manager.release(file.path)

    def is_locked(self, file: File) -> bool:
        return file.locked
