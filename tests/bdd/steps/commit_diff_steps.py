import requests
from behave import given, when

API_URL = "http://localhost:5000"
DEFAULT_USER = "alice"


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
