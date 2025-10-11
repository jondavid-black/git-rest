import requests
from behave import when, then, given

API_URL = "http://localhost:5000"

@when('I POST to /repos/{repo_id}/commit with message "{message}" and author "{author}"')
def step_impl(context, repo_id, message, author):
    context.response = requests.post(f"{API_URL}/repos/{repo_id}/commit/", json={"message": message, "author": author})

@when('I GET /repos/{repo_id}/diff')
def step_impl(context, repo_id):
    context.response = requests.get(f"{API_URL}/repos/{repo_id}/diff/")

@when('I GET /repos/{repo_id}/diff?a={commit_a}&b={commit_b}')
def step_impl(context, repo_id, commit_a, commit_b):
    context.response = requests.get(f"{API_URL}/repos/{repo_id}/diff/", params={"a": commit_a, "b": commit_b})

@given('two commits exist in "{repo_id}"')
def step_impl(context, repo_id):
    # Create two commits for diff testing
    for i in range(2):
        requests.post(f"{API_URL}/repos/{repo_id}/commit/", json={"message": f"Commit {i+1}", "author": "TestUser"})

@then('the response should contain "{key}"')
def step_impl(context, key):
    data = context.response.json()
    assert key in data
