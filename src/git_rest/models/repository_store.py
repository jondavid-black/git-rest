import os

import git

from .repository import Branch, Remote, Repository, RepoStatus


class RepositoryStore:
    def init_repo(self, name: str) -> Repository:
        """
        Initialize a new git repository in the user's repo directory.
        """
        import re

        if not re.match(r"^[A-Za-z0-9_.-]+$", name):
            raise ValueError(
                "Repository name must be alphanumeric, dash, dot, or underscore"
            )
        repo_path = os.path.join(self.base_dir, name)
        if os.path.exists(repo_path):
            raise FileExistsError(f"Repository '{name}' already exists.")
        try:
            os.makedirs(repo_path, exist_ok=False)
            git.Repo.init(repo_path)
            # Optionally, create an initial README or .gitignore here if desired
            return self._load_repo(repo_path)
        except Exception as e:
            # Clean up if partial directory created
            if os.path.exists(repo_path):
                import shutil

                shutil.rmtree(repo_path, ignore_errors=True)
            raise OSError(f"Failed to initialize repository: {e}") from e

    def _load_git_repo(self, repo_path: str):
        return git.Repo(repo_path)

    def get_user_repo(self, user: str, repo_id: str) -> Repository:
        """
        Get a repository for a specific user, assuming user isolation is implemented as base_dir/user/repo_id
        """
        repo_path = os.path.normpath(os.path.join(self.base_dir, user, repo_id))
        # Prevent path traversal; ensure repo_path is a subpath of self.base_dir
        if not repo_path.startswith(self.base_dir + os.sep):
            raise FileNotFoundError(
                f"Repository '{repo_id}' for user '{user}' not found."
            )
        if not os.path.isdir(os.path.join(repo_path, ".git")):
            raise FileNotFoundError(
                f"Repository '{repo_id}' for user '{user}' not found."
            )
        return self._load_repo(repo_path)

    def __init__(self, base_dir: str | None = None):
        import logging

        self.logger = logging.getLogger(__name__)
        self.base_dir = base_dir or os.environ.get("GIT_REST_WORKDIR", "/tmp/git-rest")
        self.base_dir = os.path.abspath(self.base_dir)
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir, exist_ok=True)

    def list_repos(self) -> list[Repository]:
        repos = []
        for entry in os.listdir(self.base_dir):
            repo_path = os.path.join(self.base_dir, entry)
            if os.path.isdir(repo_path) and os.path.isdir(
                os.path.join(repo_path, ".git")
            ):
                repos.append(self._load_repo(repo_path))
        return repos

    def _load_repo(self, repo_path: str) -> Repository:
        import sys

        repo = git.Repo(repo_path)
        # Check for detached HEAD or no branches
        if repo.head.is_detached:
            print(
                f"[DEBUG] Repo at {repo_path} is in detached HEAD state.",
                file=sys.stderr,
            )
        if not repo.heads:
            print(
                f"[DEBUG] Repo at {repo_path} has no local branches.", file=sys.stderr
            )
        remotes = [Remote(name=r.name, url=r.url) for r in repo.remotes]
        try:
            branches = [
                Branch(name=b.name, is_current=(b.name == repo.active_branch.name))
                for b in repo.branches
            ]
        except Exception as e:
            print(f"[ERROR] Could not determine active branch: {e}", file=sys.stderr)
            branches = [Branch(name=b.name, is_current=False) for b in repo.branches]
        status = RepoStatus(
            staged=[],  # To be filled with actual status logic
            unstaged=[],
            untracked=[],
        )
        # Try to get the remote repo name from the 'origin' URL
        remote_name = os.path.basename(repo_path)
        try:
            origin = repo.remotes.origin
            origin_url = origin.url
            # Remove trailing .git if present
            remote_name = os.path.splitext(os.path.basename(origin_url))[0]
        except Exception:
            pass
        current_branch = None
        try:
            current_branch = repo.active_branch.name
        except Exception as e:
            print(f"[ERROR] Could not get current branch: {e}", file=sys.stderr)
        return Repository(
            id=os.path.basename(repo_path),
            name=remote_name,
            path=repo_path,
            remotes=remotes,
            branches=branches,
            current_branch=current_branch,
            status=status,
        )

    def clone_repo(self, name: str, url: str) -> Repository:
        repo_path = os.path.join(self.base_dir, name)
        if os.path.exists(repo_path):
            raise FileExistsError(f"Repository '{name}' already exists.")
        repo = git.Repo.clone_from(url, repo_path)
        # Debug: print refs, heads, remotes, and remote refs after clone
        self.logger.debug(f"After clone: repo.refs = {[ref.name for ref in repo.refs]}")
        self.logger.debug(
            f"After clone: repo.heads = {[head.name for head in repo.heads]}"
        )
        self.logger.debug(
            f"After clone: repo.branches = {[b.name for b in getattr(repo, 'branches', [])]}"
        )
        self.logger.debug(
            f"After clone: repo.remotes = {[r.name for r in repo.remotes]}"
        )
        for remote in repo.remotes:
            self.logger.debug(
                f"Remote {remote.name} refs: {[ref.name for ref in remote.refs]}"
            )

        try:
            # Try to checkout main or master if present
            main_branch = None
            for branch_name in ["main", "master"]:
                remote_branch = f"origin/{branch_name}"
                if remote_branch in [ref.name for ref in repo.refs]:
                    main_branch = branch_name
                    break
            if main_branch:
                repo.git.checkout(main_branch)
            self.logger.debug(
                f"After attempting checkout of main/master: repo.branches = {[b.name for b in repo.branches]}"
            )

            # If still no local branches, force a fetch and try again
            if not repo.branches:
                self.logger.info(
                    "No local branches after clone, fetching all remotes..."
                )
                for remote in repo.remotes:
                    remote.fetch()
                self.logger.debug(
                    f"After fetch: repo.refs = {[ref.name for ref in repo.refs]}"
                )
                self.logger.debug(
                    f"After fetch: repo.heads = {[head.name for head in repo.heads]}"
                )
                self.logger.debug(
                    f"After fetch: repo.branches = {[b.name for b in getattr(repo, 'branches', [])]}"
                )
                # Gather all remote branches except HEAD
                remote_branches = []
                for remote in repo.remotes:
                    for ref in remote.refs:
                        if (
                            ref.name.startswith(f"{remote.name}/")
                            and ref.name != f"{remote.name}/HEAD"
                        ):
                            remote_branches.append(ref)
                self.logger.debug(
                    f"After fetch: remote_branches = {[ref.name for ref in remote_branches]}"
                )
                if remote_branches:
                    # Prefer origin/main or origin/master, else first remote branch
                    preferred = None
                    for b in ["origin/main", "origin/master"]:
                        for ref in remote_branches:
                            if ref.name == b:
                                preferred = ref
                                break
                        if preferred:
                            break
                    if not preferred:
                        preferred = remote_branches[0]
                    local_branch_name = preferred.name.split("/", 1)[1]
                    commit_hash = (
                        preferred.commit.hexsha
                        if hasattr(preferred, "commit")
                        else None
                    )
                    self.logger.debug(
                        f"Fallback: creating local branch '{local_branch_name}' at commit {commit_hash} from remote ref '{preferred.name}'"
                    )
                    try:
                        # Try to create a local branch tracking the remote
                        repo.git.checkout(
                            "-b", local_branch_name, "--track", preferred.name
                        )
                        self.logger.info(
                            f"Created local branch '{local_branch_name}' tracking '{preferred.name}' after fetch."
                        )
                    except Exception as e:
                        self.logger.warning(
                            f"Could not create tracking branch, trying direct commit checkout: {e}"
                        )
                        if commit_hash:
                            repo.git.checkout("-b", local_branch_name, commit_hash)
                            self.logger.info(
                                f"Created local branch '{local_branch_name}' at commit {commit_hash} after fetch."
                            )
                        else:
                            self.logger.error(
                                f"No commit hash available for remote ref '{preferred.name}'"
                            )
                else:
                    self.logger.warning(
                        f"No remote branches found after fetch for repo {name}."
                    )
            # Final debug: log all local branches after attempted creation
            self.logger.debug(
                f"Final local branches after all attempts: {[b.name for b in repo.branches]}"
            )
        except Exception as e:
            self.logger.warning(f"Could not ensure local branch after clone/fetch: {e}")
        return self._load_repo(repo_path)

    def get_repo(self, repo_id: str) -> Repository:
        repo_path = os.path.normpath(os.path.join(self.base_dir, repo_id))
        # Prevent path traversal and ensure repo_path is within base_dir
        if not repo_path.startswith(self.base_dir + os.sep):
            raise FileNotFoundError(
                f"Repository '{repo_id}' not found."
            )  # Or use PermissionError("... not allowed")
        if not os.path.isdir(os.path.join(repo_path, ".git")):
            raise FileNotFoundError(f"Repository '{repo_id}' not found.")
        return self._load_repo(repo_path)
