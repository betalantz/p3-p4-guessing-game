#!/usr/bin/env python3
import warnings
from datetime import datetime, timedelta

from db import db
from default_config import DefaultConfig
from flask import Flask, redirect
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    current_user,
    get_jwt,
    set_access_cookies,
)
from flask_migrate import Migrate
from flask_smorest import Api
from models import TokenBlocklist, User
from resources.game import blp as GameBlueprint
from resources.user import blp as UserBlueprint
from sqlalchemy import select

app = Flask(__name__)
app.config.from_object(DefaultConfig)
app.json.compact = False

Migrate(app, db)
db.init_app(app)

# Prevent warnings about nested schemas
with app.app_context():
    warnings.filterwarnings("ignore", message="Multiple schemas resolved to the name ")


# Create JWTManager
jwt = JWTManager(app)


# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.scalars(
        select(TokenBlocklist).where(TokenBlocklist.jti == jti)
    ).one_or_none()
    return token is not None


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return {"description": "The token has been revoked.", "error": "token_revoked"}, 401


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Register a callback function that loads a user from the database whenever
# a protected route is accessed.
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_payload):
    identity = jwt_payload["sub"]  # subject of the jwt i.e. the user
    return db.session.scalars(select(User).where(User.id == identity)).one_or_none()


# Create the API
api = Api(app)

# Register blueprints
api.register_blueprint(GameBlueprint)
api.register_blueprint(UserBlueprint)

# Add authorize button to OpenAPI document
api.spec.components.security_scheme(
    "bearerAuth", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
)
# Uncomment to add lock icon to all endpoints
# api.spec.options["security"] = [{"bearerAuth": []}]

# add lock icon to endpoints documented with @blp.doc(authorize=True)
for path, items in api.spec._paths.items():
    for method in items.keys():
        endpoint = api.spec._paths[path][method]
        if type(endpoint) is dict and endpoint.get("authorize"):
            api.spec._paths[path][method]["security"] = [{"bearerAuth": []}]


@app.route("/")
def index():
    return redirect(app.config["OPENAPI_SWAGGER_UI_PATH"])


# Using an `after_request` callback, we refresh any token that is within 15
# minutes of expiring.
@app.after_request
def refresh_expiring_jwts(response):
    try:
        # print("refreshing token")
        exp_timestamp = get_jwt()["exp"]
        now = datetime.utcnow()
        target_timestamp = datetime.timestamp(now + timedelta(minutes=15))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=current_user)
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)
