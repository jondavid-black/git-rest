import os


class FileSystemIsolation:
    def __init__(self, base_dir: str | None = None):
        self.base_dir = base_dir or os.environ.get("GIT_REST_WORKDIR", "/tmp/git-rest")
        self.base_dir = os.path.abspath(self.base_dir)
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir, exist_ok=True)

    def safe_join(self, *paths) -> str:
        # Join and resolve to absolute path
        joined = os.path.abspath(os.path.join(self.base_dir, *paths))
        # Allow base_dir itself, or any subpath
        if not (joined == self.base_dir or joined.startswith(self.base_dir + os.sep)):
            raise ValueError(
                "Path traversal detected or path outside allowed directory"
            )
        return joined

    def is_safe_path(self, path: str) -> bool:
        abs_path = os.path.abspath(os.path.join(self.base_dir, path))
        return abs_path.startswith(self.base_dir + os.sep)

    def list_dir(self, rel_path: str = ""):
        dir_path = self.safe_join(rel_path)
        if not os.path.isdir(dir_path):
            raise FileNotFoundError(f"Directory not found: {rel_path}")
        return os.listdir(dir_path)

    def file_exists(self, rel_path: str) -> bool:
        return os.path.isfile(self.safe_join(rel_path))

    def dir_exists(self, rel_path: str) -> bool:
        return os.path.isdir(self.safe_join(rel_path))
