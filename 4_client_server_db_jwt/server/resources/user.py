from datetime import datetime, timezone

from db import db
from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
    current_user
)
from flask_smorest import Blueprint, abort
from models import TokenBlocklist, User
from schemas import UserSchema
from sqlalchemy import select

blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register")
class UsersRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """Add a new user."""
        user = db.session.scalars(
            select(User).where(User.name == user_data["name"])
        ).one_or_none()
        if user:
            abort(409, message="A user with that name already exists.")

        user = User(
            name=user_data["name"],
            password=user_data["password"],
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
        ).one_or_none()
        if user and user.authenticate(user_data["password"]):
            # pass actual user object for automatic user loading, not just id
            # access_token = create_access_token(identity=user.id)
            access_token = create_access_token(identity=user)
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
        
        #user_id = get_jwt_identity()
        #access_token = create_access_token(identity=user_id)
        access_token = create_access_token(identity=current_user)
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
    
@blp.route("/users")
class UsersView(MethodView):
    
    @blp.response(200, UserSchema(many=True))
    def get(self):
        """List users"""
        return db.session.scalars(db.select(User))
