import requests
from behave import given, when

API_URL = "http://localhost:5000"


@when(
    'I POST to /repos/{repo_id}/commit with message "{message}" and author "{author}"'
)
def post_commit_with_message_and_author(context, repo_id, message, author):
    context.response = requests.post(
        f"{API_URL}/repos/{repo_id}/commit/",
        json={"message": message, "author": author},
    )


@when("I GET /repos/{repo_id}/diff")
def get_diff_for_repo(context, repo_id):
    context.response = requests.get(f"{API_URL}/repos/{repo_id}/diff/")


@when("I GET /repos/{repo_id}/diff?a={commit_a}&b={commit_b}")
def get_diff_between_commits(context, repo_id, commit_a, commit_b):
    # Use commit hashes from context if available
    a = getattr(context, "commit_a", commit_a)
    b = getattr(context, "commit_b", commit_b)
    context.response = requests.get(
        f"{API_URL}/repos/{repo_id}/diff/", params={"a": a, "b": b}
    )


@given('two commits exist in "{repo_id}"')
def given_two_commits_exist(context, repo_id):
    # Create two commits and store their hashes for diff testing
    hashes = []
    for i in range(2):
        resp = requests.post(
            f"{API_URL}/repos/{repo_id}/commit/",
            json={"message": f"Commit {i + 1}", "author": "TestUser"},
        )
        if resp.status_code == 201:
            hashes.append(resp.json()["hash"])
    if len(hashes) == 2:
        context.commit_a = hashes[0]
        context.commit_b = hashes[1]
