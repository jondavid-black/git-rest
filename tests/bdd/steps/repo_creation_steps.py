import os
import requests
from behave import given, when, then

API_URL = "http://localhost:5000/api/repos"
REPO_DIR = "test_working_dir/JD/"


@given('a repository named "{repo_name}" already exists')
def given_repo_already_exists(context, repo_name):
    repo_path = os.path.join(REPO_DIR, repo_name)
    if not os.path.exists(repo_path):
        payload = {"name": repo_name, "description": "Pre-existing repo"}
        requests.post(API_URL, json=payload)

@when('I POST to /api/repos with name "{name}", description "{description}", license "{license}", and README "{readme}"')
def when_post_create_repo_full(context, name, description, license, readme):
    payload = {"name": name, "description": description, "license": license, "readme": readme}
    context.response = requests.post(API_URL, json=payload)

@when('I POST to /api/repos with name "{name}"')
def when_post_create_repo_minimal(context, name):
    payload = {"name": name}
    context.response = requests.post(API_URL, json=payload)


@then('the response should contain "{field1}", "{field2}", "{field3}", and "{field4}"')
def then_response_should_contain_fields(context, field1, field2, field3, field4):
    data = context.response.json()
    for field in [field1, field2, field3, field4]:
        assert field in data

@then('a directory "{dir}" should exist')
def then_directory_should_exist(context, dir):
    assert os.path.exists(dir)

@then('the files "{file1}" and "{file2}" should exist in that directory')
def then_files_should_exist_in_directory(context, file1, file2):
    repo_path = context.response.json()["name"]
    dir_path = os.path.join(REPO_DIR, repo_path)
    assert os.path.isfile(os.path.join(dir_path, file1))
    assert os.path.isfile(os.path.join(dir_path, file2))

