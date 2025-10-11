import requests
from behave import then, when

API_URL = "http://localhost:5000"


@when("I GET /repos/{repo_id}/branches")
def when_get_repos_repo_id_branches(context, repo_id):
    context.response = requests.get(f"{API_URL}/repos/{repo_id}/branches/")


@when('I POST to /repos/{repo_id}/branches with name "{branch_name}"')
def when_post_repos_repo_id_branches_with_name(context, repo_id, branch_name):
    context.response = requests.post(
        f"{API_URL}/repos/{repo_id}/branches/", json={"name": branch_name}
    )


@when("I POST to /repos/{repo_id}/branches/{branch}")
def when_post_repos_repo_id_branches_branch(context, repo_id, branch):
    context.response = requests.post(f"{API_URL}/repos/{repo_id}/branches/{branch}")


@when("I DELETE /repos/{repo_id}/branches/{branch}")
def when_delete_repos_repo_id_branches_branch(context, repo_id, branch):
    context.response = requests.delete(f"{API_URL}/repos/{repo_id}/branches/{branch}")


@then('the response should contain a branch named "{branch_name}"')
def then_response_should_contain_branch_named(context, branch_name):
    data = context.response.json()
    assert any(b.get("name") == branch_name for b in data)


@then('the response should not contain a branch named "{branch_name}"')
def then_response_should_not_contain_branch_named(context, branch_name):
    data = context.response.json()
    assert all(b.get("name") != branch_name for b in data)
