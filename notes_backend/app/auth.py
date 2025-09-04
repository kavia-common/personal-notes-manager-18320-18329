import time
from typing import Tuple

from flask import current_app, request
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from werkzeug.exceptions import Unauthorized


def _get_serializer() -> URLSafeTimedSerializer:
    """Create itsdangerous serializer using Flask secret key."""
    secret = current_app.config["SECRET_KEY"]
    return URLSafeTimedSerializer(secret_key=secret, salt="notes-auth")


# PUBLIC_INTERFACE
def create_access_token(identity: str) -> str:
    """Create a time-bound signed token for the given identity (email).

    The token is signed using Flask SECRET_KEY and includes iat (issued at).
    """
    s = _get_serializer()
    payload = {"sub": identity, "iat": int(time.time())}
    token = s.dumps(payload)
    return token


def _decode_token(token: str) -> Tuple[str, dict]:
    """Decode and validate the token, returning subject and payload."""
    s = _get_serializer()
    max_age = int(current_app.config["ACCESS_TOKEN_EXPIRES_MINUTES"]) * 60
    try:
        payload = s.loads(token, max_age=max_age)
        sub = payload.get("sub")
        if not sub:
            raise Unauthorized("Invalid token payload")
        return sub, payload
    except SignatureExpired as exc:
        raise Unauthorized("Token expired") from exc
    except BadSignature as exc:
        raise Unauthorized("Invalid token") from exc


# PUBLIC_INTERFACE
def get_current_identity() -> str:
    """Extract and validate Authorization: Bearer token and return identity (email)."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise Unauthorized("Missing or invalid Authorization header")
    token = auth_header.split(" ", 1)[1].strip()
    sub, _ = _decode_token(token)
    return sub


# PUBLIC_INTERFACE
def require_auth() -> str:
    """Require authenticated user; returns identity (email) or raises Unauthorized."""
    return get_current_identity()
