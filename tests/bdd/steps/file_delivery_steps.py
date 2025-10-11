import os

import requests
from behave import given, then, when

API_URL = "http://localhost:5000"
DEFAULT_USER = "alice"


@when("I GET /users/{user_id}/repos/{repo_id}/files")
def get_files_for_repo(context, user_id, repo_id):
    context.response = requests.get(f"{API_URL}/users/{user_id}/repos/{repo_id}/files/")


@when("I GET /users/{user_id}/repos/{repo_id}/files/{file_path}")
def get_file_from_repo(context, user_id, repo_id, file_path):
    context.response = requests.get(
        f"{API_URL}/users/{user_id}/repos/{repo_id}/files/{file_path}"
    )


@given('a large file named "{filename}" exists in "users/{user_id}/{repo_id}"')
def given_large_file_exists(context, filename, user_id, repo_id):
    repo_path = os.path.join("/tmp/git-rest", user_id, repo_id)
    os.makedirs(repo_path, exist_ok=True)
    file_path = os.path.join(repo_path, filename)
    with open(file_path, "wb") as f:
        f.write(os.urandom(2 * 1024 * 1024))  # 2MB file


@then("the response should contain file content")
def then_response_should_contain_file_content(context):
    assert context.response.content


@given('a secure URL for "{filename}" in "users/{user_id}/{repo_id}"')
def given_secure_url_for_file(context, filename, user_id, repo_id):
    resp = requests.get(f"{API_URL}/users/{user_id}/repos/{repo_id}/files/{filename}")
    data = resp.json()
    context.secure_url = f"{API_URL}{data['url']}"


@when("I GET the secure URL")
def get_secure_url(context):
    context.response = requests.get(context.secure_url)


@then('the response should contain "diff"')
def step_impl_response_should_contain_diff(context):
    data = context.response.json()
    assert "diff" in data, "Response does not contain 'diff' key"


@then('the response should contain "url"')
def step_impl_response_should_contain_url(context):
    data = context.response.json()
    assert "url" in data, "Response does not contain 'url' key"
