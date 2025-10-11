import requests
from behave import when, then, given
import os

API_URL = "http://localhost:5000"

@when('I GET /repos/{repo_id}/files')
def step_impl(context, repo_id):
    context.response = requests.get(f"{API_URL}/repos/{repo_id}/files/")

@when('I GET /repos/{repo_id}/files/{file_path}')
def step_impl(context, repo_id, file_path):
    context.response = requests.get(f"{API_URL}/repos/{repo_id}/files/{file_path}")

@given('a large file named "{filename}" exists in "{repo_id}"')
def step_impl(context, filename, repo_id):
    # Create a large file in the repo for testing
    repo_path = os.path.join("/tmp/git-rest", repo_id)
    file_path = os.path.join(repo_path, filename)
    with open(file_path, "wb") as f:
        f.write(os.urandom(2 * 1024 * 1024))  # 2MB file

@then('the response should contain file content')
def step_impl(context):
    assert context.response.content

@then('the response should contain "{key}"')
def step_impl(context, key):
    data = context.response.json()
    assert key in data

@given('a secure URL for "{filename}" in "{repo_id}"')
def step_impl(context, filename, repo_id):
    # Get secure URL from API
    resp = requests.get(f"{API_URL}/repos/{repo_id}/files/{filename}")
    data = resp.json()
    context.secure_url = f"{API_URL}{data['url']}"

@when('I GET the secure URL')
def step_impl(context):
    context.response = requests.get(context.secure_url)
