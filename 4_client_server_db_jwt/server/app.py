#!/usr/bin/env python3
from flask import Flask, redirect, jsonify
from flask_migrate import Migrate
from flask_smorest import Api
from flask_jwt_extended import JWTManager
import warnings

from db import db
from default_config import DefaultConfig
from resources.game import blp as GameBlueprint
from resources.user import blp as UserBlueprint
from blocklist import BLOCKLIST

app = Flask(__name__)
app.config.from_object(DefaultConfig)
app.json.compact = False

Migrate(app, db)
db.init_app(app)

# Ensure FOREIGN KEY for sqlite3
if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
    def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
        dbapi_con.execute('pragma foreign_keys=ON')

    with app.app_context():
        from sqlalchemy import event
        event.listen(db.engine, 'connect', _fk_pragma_on_connect)

# Prevent warnings about nested schemas
with app.app_context():
    warnings.filterwarnings(
            "ignore",
            message="Multiple schemas resolved to the name "
        )


# Create JWTManager
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )

# Create the API
api = Api(app)
api.spec.components.security_scheme(
    "bearerAuth", {"type":"http", "scheme": "bearer", "bearerFormat": "JWT"}
)
#api.spec.options["security"] = [{"bearerAuth": []}]
api.register_blueprint(GameBlueprint)
api.register_blueprint(UserBlueprint)

#add lock icon for jwt endpoint 
for path, items in api.spec._paths.items():
        for method in items.keys():
            endpoint = api.spec._paths[path][method]
            if type(endpoint) is dict and endpoint.get("authorize"):
                api.spec._paths[path][method]["security"] = [{"bearerAuth": []}]
    
@app.route('/')
def index():
    return redirect(app.config["OPENAPI_SWAGGER_UI_PATH"])

if __name__ == '__main__':
    app.run(port=5555, debug=True)
