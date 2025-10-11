import os
import git
from typing import List, Optional
from models.repository import Repository, Remote, Branch, RepoStatus, FileEntry
from datetime import datetime

class RepositoryStore:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or os.environ.get("GIT_REST_WORKDIR", "/tmp/git-rest")
        self.base_dir = os.path.abspath(self.base_dir)
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir, exist_ok=True)

    def list_repos(self) -> List[Repository]:
        repos = []
        for entry in os.listdir(self.base_dir):
            repo_path = os.path.join(self.base_dir, entry)
            if os.path.isdir(repo_path) and os.path.isdir(os.path.join(repo_path, ".git")):
                repos.append(self._load_repo(repo_path))
        return repos

    def _load_repo(self, repo_path: str) -> Repository:
        repo = git.Repo(repo_path)
        remotes = [Remote(name=r.name, url=r.url) for r in repo.remotes]
        branches = [Branch(name=b.name, is_current=(b.name == repo.active_branch.name)) for b in repo.branches]
        status = RepoStatus(
            staged=[],  # To be filled with actual status logic
            unstaged=[],
            untracked=[]
        )
        return Repository(
            id=os.path.basename(repo_path),
            name=os.path.basename(repo_path),
            path=repo_path,
            remotes=remotes,
            branches=branches,
            current_branch=repo.active_branch.name,
            status=status
        )

    def clone_repo(self, name: str, url: str) -> Repository:
        repo_path = os.path.join(self.base_dir, name)
        if os.path.exists(repo_path):
            raise FileExistsError(f"Repository '{name}' already exists.")
        repo = git.Repo.clone_from(url, repo_path)
        return self._load_repo(repo_path)

    def get_repo(self, repo_id: str) -> Repository:
        repo_path = os.path.join(self.base_dir, repo_id)
        if not os.path.isdir(os.path.join(repo_path, ".git")):
            raise FileNotFoundError(f"Repository '{repo_id}' not found.")
        return self._load_repo(repo_path)
