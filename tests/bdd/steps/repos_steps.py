import requests
from behave import when

API_URL = "http://localhost:5000"


@when('I POST to /repos with name "{name}" and url "{url}"')
def post_repos_with_name_and_url(context, name, url):
    context.response = requests.post(
        f"{API_URL}/repos/", json={"name": name, "url": url}
    )


@when("I GET /repos")
def get_repos(context):
    context.response = requests.get(f"{API_URL}/repos/")


@when("I GET /repos/{repo_id}")
def get_repo_by_id(context, repo_id):
    context.response = requests.get(f"{API_URL}/repos/{repo_id}")


@when("I POST to /repos/{repo_id}")
def post_to_repo_by_id(context, repo_id):
    context.response = requests.post(f"{API_URL}/repos/{repo_id}")
