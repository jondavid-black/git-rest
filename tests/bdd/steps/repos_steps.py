import time

import requests
from behave import then, when

API_URL = "http://localhost:5000"
DEFAULT_USER = "alice"


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
