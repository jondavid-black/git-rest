from functools import wraps
from flask import request, jsonify, current_app
import jwt
import os
from datetime import datetime, timedelta

# Example secret key usage (should be set via env)
SECRET_KEY = os.environ.get("GIT_REST_SECRET_KEY", "changeme-super-secret-key")

# Dummy user store for demonstration (replace with real user management)
USERS = {
    "admin": "password123"
}

def generate_token(username: str, expires_in: int = 3600):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
        token = auth_header.split(" ", 1)[1]
        user = decode_token(token)
        if not user:
            return jsonify({"error": "Invalid or expired token"}), 401
        request.user = user
        return f(*args, **kwargs)
    return decorated

# Example login endpoint (to be registered in Flask app)
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if USERS.get(username) == password:
        token = generate_token(username)
        return jsonify({"access_token": token})
    return jsonify({"error": "Invalid credentials"}), 401
