import os

import requests
from behave import given, then

API_URL = "http://localhost:5000"


@given("the API is running")
def step_impl_api_running(context):
    resp = requests.get(f"{API_URL}/healthz")
    assert resp.status_code == 200


@given('a repository named "{repo_name}" exists')
def step_impl_repo_exists(context, repo_name):
    import subprocess

    repo_path = os.path.join("/tmp/git-rest", repo_name)
    if not os.path.exists(repo_path):
        os.makedirs(repo_path, exist_ok=True)
        subprocess.run(["git", "init"], cwd=repo_path, check=True)
        # Create an initial commit so the default branch exists
        with open(os.path.join(repo_path, "README.md"), "w") as f:
            f.write(f"# {repo_name}\n")
        subprocess.run(["git", "add", "README.md"], cwd=repo_path, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"], cwd=repo_path, check=True
        )


@then("the response status should be {status:d}")
def step_impl_response_status(context, status):
    actual = context.response.status_code
    print(f"[BDD] Response status: actual={actual}, expected={status}")
    if actual != status:
        print(f"[BDD] Response body: {context.response.text}")
    assert actual == status


@then("the response should be a list")
def step_impl_response_should_be_list(context):
    data = context.response.json()
    assert isinstance(data, list)


@then('the response should contain "{key}": "{value}"')
def step_impl_response_should_contain_key_value(context, key, value):
    data = context.response.json()
    assert key in data
    assert str(data[key]) == value
