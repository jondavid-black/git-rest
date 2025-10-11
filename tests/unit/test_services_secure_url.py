import time

from git_rest.services.secure_url import SecureURLGenerator


def test_generate_and_verify_nominal():
    gen = SecureURLGenerator(secret="test-secret")
    repo_id = "repo1"
    file_path = "file.txt"
    url = gen.generate(repo_id, file_path, expires_in=10)
    # Extract params from URL
    assert url.startswith(f"/repos/{repo_id}/files/{file_path}?")
    import urllib.parse

    params = url.split("?")[1]
    param_dict = dict(p.split("=") for p in params.split("&"))
    expires = param_dict["expires"]
    token = urllib.parse.unquote(param_dict["token"])
    assert gen.verify(repo_id, file_path, expires, token)


def test_verify_expired():
    gen = SecureURLGenerator(secret="test-secret")
    repo_id = "repo1"
    file_path = "file.txt"
    expires = str(int(time.time()) - 10)  # already expired
    token = gen.generate(repo_id, file_path, expires_in=-10).split("token=")[1]
    assert not gen.verify(repo_id, file_path, expires, token)


def test_verify_invalid_token():
    gen = SecureURLGenerator(secret="test-secret")
    repo_id = "repo1"
    file_path = "file.txt"
    expires = str(int(time.time()) + 10)
    token = "invalidtoken"
    assert not gen.verify(repo_id, file_path, expires, token)
