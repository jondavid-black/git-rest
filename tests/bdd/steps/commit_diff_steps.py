import os
import subprocess

import requests
from behave import given, then, when

API_URL = "http://localhost:5000"
DEFAULT_USER = "alice"


# Step to detach HEAD in a repo (for edge case scenario)
@when('I detach HEAD in repo "{repo_name}"')
def step_impl_detach_head(context, repo_name):
    user_id = getattr(context, "user_id", "alice")
    repo_path = os.path.join("/tmp/git-rest", user_id, repo_name)
    # Get the latest commit hash
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo_path, capture_output=True, text=True
    )
    commit_hash = result.stdout.strip()
    # Checkout the commit hash to detach HEAD
    subprocess.run(["git", "checkout", commit_hash], cwd=repo_path, check=True)


@when(
    'I POST to /users/{user_id}/repos/{repo_id}/commit with message "{message}" and author "{author}"'
)
def post_commit_with_message_and_author(context, user_id, repo_id, message, author):
    context.response = requests.post(
        f"{API_URL}/users/{user_id}/repos/{repo_id}/commit/",
        json={"message": message, "author": author},
    )


@when("I GET /users/{user_id}/repos/{repo_id}/diff")
def get_diff_for_repo(context, user_id, repo_id):
    context.response = requests.get(f"{API_URL}/users/{user_id}/repos/{repo_id}/diff/")


@when("I GET /users/{user_id}/repos/{repo_id}/diff?a={commit_a}&b={commit_b}")
def get_diff_between_commits(context, user_id, repo_id, commit_a, commit_b):
    a = getattr(context, "commit_a", commit_a)
    b = getattr(context, "commit_b", commit_b)
    context.response = requests.get(
        f"{API_URL}/users/{user_id}/repos/{repo_id}/diff/", params={"a": a, "b": b}
    )


@given('two commits exist in "users/{user_id}/{repo_id}"')
def given_two_commits_exist(context, user_id, repo_id):
    hashes = []
    for i in range(2):
        resp = requests.post(
            f"{API_URL}/users/{user_id}/repos/{repo_id}/commit/",
            json={"message": f"Commit {i + 1}", "author": "TestUser"},
        )
        if resp.status_code == 201:
            hashes.append(resp.json()["hash"])
    if len(hashes) == 2:
        context.commit_a = hashes[0]
        context.commit_b = hashes[1]


@then('the response should not contain "{text}"')
def step_impl_response_should_not_contain_text(context, text):
    # Try JSON, fallback to text
    try:
        data = context.response.json()

        # Check all string values in JSON for the text
        def contains(d):
            if isinstance(d, dict):
                return any(contains(v) for v in d.values())
            if isinstance(d, list):
                return any(contains(v) for v in d)
            if isinstance(d, str):
                return text in d
            return False

        assert not contains(data), f'Found "{text}" in JSON response: {data}'
    except Exception:
        body = context.response.text
        assert text not in body, f'Found "{text}" in response body: {body}'
