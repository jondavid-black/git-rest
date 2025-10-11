import base64
import hashlib
import hmac
import os
import time
from urllib.parse import urlencode


class SecureURLGenerator:
    def __init__(self, secret=None):
        self.secret = secret or os.environ.get(
            "GIT_REST_SECRET_KEY", "changeme-super-secret-key"
        )

    def generate(self, repo_id, file_path, expires_in=300):
        expires = int(time.time()) + expires_in
        data = f"{repo_id}:{file_path}:{expires}"
        sig = hmac.new(self.secret.encode(), data.encode(), hashlib.sha256).digest()
        token = base64.urlsafe_b64encode(sig).decode()
        params = urlencode({"expires": expires, "token": token})
        return f"/repos/{repo_id}/files/{file_path}?{params}"

    def verify(self, repo_id, file_path, expires, token):
        data = f"{repo_id}:{file_path}:{expires}"
        expected_sig = hmac.new(
            self.secret.encode(), data.encode(), hashlib.sha256
        ).digest()
        expected_token = base64.urlsafe_b64encode(expected_sig).decode()
        if token != expected_token:
            return False
        if int(expires) < int(time.time()):
            return False
        return True
