from datetime import datetime, timezone

from db import db
from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)
from flask_smorest import Blueprint, abort
from models import TokenBlocklist, User
from passlib.hash import pbkdf2_sha256
from schemas import UserSchema
from sqlalchemy import select

blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register")
class UsersRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """Add a new user."""
        # if User.query.filter(User.name == user_data["name"]).first():
        user = db.session.scalars(
            select(User).where(User.name == user_data["name"])
        ).first()
        if user:
            abort(409, message="A user with that name already exists.")

        user = User(
            name=user_data["name"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201


@blp.route("/login")
class UsersLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """Create and return access token for registered user."""
        user = db.session.scalars(
            select(User).where(User.name == user_data["name"])
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            resp = jsonify({"access_token": access_token})

            # Set the JWT access cookie in the response
            set_access_cookies(resp, access_token)
            return resp, 200

        abort(401, message="Invalid credentials.")


# TODO: add refresh token route, see if /authenticate is needed
@blp.route("/authenticate")
class UserAuthenticated(MethodView):
    # be default, jwt_required() checks for type="access" token
    @jwt_required()
    @blp.doc(authorize=True)
    def get(self):
        """Check if user is authenticated."""
        # looks like much of below is handled by token_in_blocklist_loader
        # so just sending new access token back to client for now
        # jti = get_jwt()["jti"]
        # blocked = db.session.scalars(
        #     select(TokenBlocklist).where(TokenBlocklist.jti == jti)
        # ).first()
        # if blocked:
        #     abort(401, message="Token has been revoked.")
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        resp = jsonify({"access_token": access_token})
        set_access_cookies(resp, access_token)
        return resp, 200


@blp.route("/logout")
class UsersLogout(MethodView):
    @jwt_required()
    @blp.doc(authorize=True)
    def post(self):
        """Revoke access token for authenticated user."""
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()
        resp = jsonify({"message": "JWT Revoked"})
        # B/c access cookie is httponly, it cannot be deleted by client-side JavaScript, so this helper function is provided to delete the cookie.
        unset_jwt_cookies(resp)
        return resp, 200
