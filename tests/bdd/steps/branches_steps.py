import requests
from behave import when, then

API_URL = "http://localhost:5000"

@when('I GET /repos/{repo_id}/branches')
def step_impl(context, repo_id):
    context.response = requests.get(f"{API_URL}/repos/{repo_id}/branches/")

@when('I POST to /repos/{repo_id}/branches with name "{branch_name}"')
def step_impl(context, repo_id, branch_name):
    context.response = requests.post(f"{API_URL}/repos/{repo_id}/branches/", json={"name": branch_name})

@when('I POST to /repos/{repo_id}/branches/{branch}')
def step_impl(context, repo_id, branch):
    context.response = requests.post(f"{API_URL}/repos/{repo_id}/branches/{branch}")

@when('I DELETE /repos/{repo_id}/branches/{branch}')
def step_impl(context, repo_id, branch):
    context.response = requests.delete(f"{API_URL}/repos/{repo_id}/branches/{branch}")

@then('the response should contain a branch named "{branch_name}"')
def step_impl(context, branch_name):
    data = context.response.json()
    assert any(b.get("name") == branch_name for b in data)

@then('the response should not contain a branch named "{branch_name}"')
def step_impl(context, branch_name):
    data = context.response.json()
    assert all(b.get("name") != branch_name for b in data)
