import requests
from behave import when

API_URL = "http://localhost:5000"
DEFAULT_USER = "alice"


@when('I POST to /users/{user_id}/repos with name "{name}" and url "{url}"')
def post_repos_with_name_and_url(context, user_id, name, url):
    context.response = requests.post(
        f"{API_URL}/users/{user_id}/repos/", json={"name": name, "url": url}
    )


@when("I GET /users/{user_id}/repos")
def get_repos(context, user_id):
    context.response = requests.get(f"{API_URL}/users/{user_id}/repos/")


@when("I GET /users/{user_id}/repos/{repo_id}")
def get_repo_by_id(context, user_id, repo_id):
    context.response = requests.get(f"{API_URL}/users/{user_id}/repos/{repo_id}")


@when("I POST to /users/{user_id}/repos/{repo_id}")
def post_to_repo_by_id(context, user_id, repo_id):
    context.response = requests.post(f"{API_URL}/users/{user_id}/repos/{repo_id}")
