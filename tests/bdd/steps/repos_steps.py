import requests
from behave import given, when, then

API_URL = "http://localhost:5000"

@given('the API is running')
def step_impl(context):
    # Optionally, check health endpoint
    resp = requests.get(f"{API_URL}/healthz")
    assert resp.status_code == 200

@when('I POST to /repos with name "{name}" and url "{url}"')
def step_impl(context, name, url):
    context.response = requests.post(f"{API_URL}/repos/", json={"name": name, "url": url})

@when('I GET /repos')
def step_impl(context):
    context.response = requests.get(f"{API_URL}/repos/")

@when('I GET /repos/{repo_id}')
def step_impl(context, repo_id):
    context.response = requests.get(f"{API_URL}/repos/{repo_id}")

@when('I POST to /repos/{repo_id}')
def step_impl(context, repo_id):
    context.response = requests.post(f"{API_URL}/repos/{repo_id}")

@then('the response status should be {status:d}')
def step_impl(context, status):
    assert context.response.status_code == status

@then('the response should contain "{key}": "{value}"')
def step_impl(context, key, value):
    data = context.response.json()
    assert key in data
    assert str(data[key]) == value

@then('the response should be a list')
def step_impl(context):
    data = context.response.json()
    assert isinstance(data, list)
