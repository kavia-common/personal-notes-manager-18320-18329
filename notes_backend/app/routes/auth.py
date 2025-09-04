from flask.views import MethodView
from flask_smorest import Blueprint
from werkzeug.exceptions import Unauthorized

from ..auth import create_access_token, require_auth
from ..repository import UserRepository
from ..schemas import UserRegisterSchema, UserLoginSchema, UserSchema, TokenSchema

blp = Blueprint("Auth", "auth", url_prefix="/auth", description="Authentication endpoints")


@blp.route("/register")
class Register(MethodView):
    """Register a new user."""

    @blp.arguments(UserRegisterSchema, location="json")
    @blp.response(201, UserSchema)
    @blp.doc(summary="Register", description="Create a new user account with email and password.")
    def post(self, data):
        """Register a new user and return user info."""
        user = UserRepository.create_user(email=data["email"], password=data["password"])
        return user


@blp.route("/login")
class Login(MethodView):
    """Login to obtain an access token."""

    @blp.arguments(UserLoginSchema, location="json")
    @blp.response(200, TokenSchema)
    @blp.doc(summary="Login", description="Authenticate with email and password to receive an access token.")
    def post(self, data):
        """Authenticate and return a bearer token."""
        user = UserRepository.get_by_email(data["email"])
        if not user or not user.check_password(data["password"]):
            raise Unauthorized("Invalid credentials")
        token = create_access_token(identity=user.email)
        return {"access_token": token}


@blp.route("/me")
class Me(MethodView):
    """Return current user's profile based on token."""

    @blp.response(200, UserSchema)
    @blp.doc(summary="Profile", description="Get current authenticated user's profile using bearer token.")
    def get(self):
        """Get current user profile."""
        email = require_auth()
        user = UserRepository.get_by_email(email)
        return user
