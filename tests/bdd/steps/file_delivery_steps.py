import os

import requests
from behave import given, then, when

API_URL = "http://localhost:5000"


@when("I GET /repos/{repo_id}/files")
def get_files_for_repo(context, repo_id):
    context.response = requests.get(f"{API_URL}/repos/{repo_id}/files/")


@when("I GET /repos/{repo_id}/files/{file_path}")
def get_file_from_repo(context, repo_id, file_path):
    context.response = requests.get(f"{API_URL}/repos/{repo_id}/files/{file_path}")


@given('a large file named "{filename}" exists in "{repo_id}"')
def given_large_file_exists(context, filename, repo_id):
    # Create a large file in the repo for testing
    repo_path = os.path.join("/tmp/git-rest", repo_id)
    file_path = os.path.join(repo_path, filename)
    with open(file_path, "wb") as f:
        f.write(os.urandom(2 * 1024 * 1024))  # 2MB file


@then("the response should contain file content")
def then_response_should_contain_file_content(context):
    assert context.response.content


@given('a secure URL for "{filename}" in "{repo_id}"')
def given_secure_url_for_file(context, filename, repo_id):
    # Get secure URL from API
    resp = requests.get(f"{API_URL}/repos/{repo_id}/files/{filename}")
    data = resp.json()
    context.secure_url = f"{API_URL}{data['url']}"


@when("I GET the secure URL")
def get_secure_url(context):
    context.response = requests.get(context.secure_url)


@then('the response should contain "diff"')
def step_impl_response_should_contain_diff(context):
    # Check that the response JSON contains a 'diff' key
    data = context.response.json()
    assert "diff" in data, "Response does not contain 'diff' key"


@then('the response should contain "url"')
def step_impl_response_should_contain_url(context):
    # Check that the response JSON contains a 'url' key
    data = context.response.json()
    assert "url" in data, "Response does not contain 'url' key"
