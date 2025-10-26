# --- Multi-repo scenario custom steps ---
import os
import shutil
import time

import requests
from behave import given, then, when


@given("I have a clean environment")
def given_i_have_a_clean_environment(context):
    # Remove /tmp/git-rest/alice if it exists
    user_id = getattr(context, "user_id", "alice")
    user_dir = os.path.join("/tmp/git-rest", user_id)
    if os.path.exists(user_dir):
        shutil.rmtree(user_dir)


@then(
    'both repositories "git-rest-test" and "git-rest-test-other" should exist for user "alice"'
)
def then_both_repos_should_exist_for_user_alice(context):
    user_id = "alice"
    base_dir = os.path.join("/tmp/git-rest", user_id)
    for repo in ["git-rest-test", "git-rest-test-other"]:
        repo_path = os.path.join(base_dir, repo)
        assert os.path.isdir(repo_path), f"Repository directory missing: {repo_path}"
        assert os.path.isdir(os.path.join(repo_path, ".git")), (
            f".git missing in {repo_path}"
        )


@then('the response should contain the correct status for "git-rest-test"')
def then_response_should_contain_correct_status_git_rest_test(context):
    data = context.response.json()
    # Acceptable keys: branch, commit, is_clean, etc. Adjust as needed.
    assert "branch" in data, "Missing 'branch' in status response"
    assert "is_clean" in data, "Missing 'is_clean' in status response"
    # Optionally check branch name or other details


@then('the response should contain the correct status for "git-rest-test-other"')
def then_response_should_contain_correct_status_git_rest_test_other(context):
    data = context.response.json()
    assert "branch" in data, "Missing 'branch' in status response"
    assert "is_clean" in data, "Missing 'is_clean' in status response"


API_URL = "http://localhost:5000"
DEFAULT_USER = "alice"


# Step for POST to /users/{user_id}/repos/clone with name and url
@when('I POST to /users/{user_id}/repos/clone with name "{name}" and url "{url}"')
def post_repos_clone_with_name_and_url(context, user_id, name, url):
    context.response = requests.post(
        f"{API_URL}/users/{user_id}/repos/clone", json={"name": name, "url": url}
    )
    # Save the url for later origin checks
    if not hasattr(context, "repo_urls"):
        context.repo_urls = {}
    context.repo_urls[name] = url


# Generic step for POST to /users/{user_id}/repos with name and url
@when('I POST to /users/{user_id}/repos with name "{name}" and url "{url}"')
def post_repos_with_name_and_url(context, user_id, name, url):
    context.response = requests.post(
        f"{API_URL}/users/{user_id}/repos", json={"name": name, "url": url}
    )
    # Save the url for later origin checks
    if not hasattr(context, "repo_urls"):
        context.repo_urls = {}
    context.repo_urls[name] = url


# Generic step for GET /users/{user_id}/repos
@when("I GET /users/{user_id}/repos")
def get_repos(context, user_id):
    context.response = requests.get(f"{API_URL}/users/{user_id}/repos")


@when('I measure the time to switch to repo "{repo_name}"')
def step_impl_measure_switch_time(context, repo_name):
    user_id = getattr(context, "user_id", "alice")
    start = time.time()
    context.response = requests.post(f"{API_URL}/users/{user_id}/repos/{repo_name}")
    end = time.time()
    context.switch_duration = end - start


@then("the switch duration should be less than 2 seconds")
def step_impl_switch_duration_under_2s(context):
    assert context.switch_duration < 2.0, (
        f"Switch took {context.switch_duration:.3f}s, expected < 2s"
    )


@when("I GET /users/{user_id}/repos/{repo_id}")
def get_repo_by_id(context, user_id, repo_id):
    context.response = requests.get(f"{API_URL}/users/{user_id}/repos/{repo_id}")


@when("I POST to /users/{user_id}/repos/{repo_id}")
def post_to_repo_by_id(context, user_id, repo_id):
    context.response = requests.post(f"{API_URL}/users/{user_id}/repos/{repo_id}")


@when("I check the response")
def step_impl(context):
    print(f"[BDD] Response body: {context.response.text}")


@then('the response should contain the correct origin for "{repo_name}"')
def step_impl_response_should_contain_correct_origin(context, repo_name):
    data = context.response.json()
    expected_url = context.repo_urls[repo_name]
    assert "origin" in data
    assert data["origin"] == expected_url, (
        f"Expected {expected_url}, got {data['origin']}"
    )


# Step for POST to /users/{user_id}/repos/init with name
@when('I POST to the init endpoint for user "{user_id}" with repo name "{name}"')
def post_init_endpoint_with_name(context, user_id, name):
    context.response = requests.post(
        f"{API_URL}/users/{user_id}/repos/init", json={"name": name}
    )


@then('the response should contain a repository named "{repo_name}"')
def then_response_should_contain_repo_named(context, repo_name):
    data = context.response.json()
    # Accepts both list of dicts or dicts with 'name' key
    if isinstance(data, list):
        names = [r["name"] for r in data if "name" in r]
        assert repo_name in names, f"Expected repo '{repo_name}' in {names}"
    elif isinstance(data, dict):
        assert data.get("name") == repo_name, f"Expected repo '{repo_name}' in {data}"
    else:
        raise AssertionError(f"Unexpected response format: {data}")
