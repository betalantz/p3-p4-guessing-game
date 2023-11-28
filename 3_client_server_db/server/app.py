#!/usr/bin/env python3
import warnings

from default_config import DefaultConfig
from flask import Flask, redirect
from flask_smorest import Api
from resources import blp as GameBlueprint

app = Flask(__name__)
app.config.from_object(DefaultConfig)
app.json.compact = False


# Prevent warnings about nested schemas
with app.app_context():
    warnings.filterwarnings("ignore", message="Multiple schemas resolved to the name ")

# Create the API
api = Api(app)
api.register_blueprint(GameBlueprint)


@app.route("/")
def index():
    return redirect(app.config["OPENAPI_SWAGGER_UI_PATH"])


if __name__ == "__main__":
    from seed import seed

    seed()

    app.run(port=5555)
