#!/usr/bin/env python3
from flask import Flask, redirect
from flask_smorest import Api

from default_config import DefaultConfig
from view import blp as GameBlueprint

app = Flask(__name__)
app.config.from_object(DefaultConfig)
app.json.compact = False

# Create the API
api = Api(app)
api.register_blueprint(GameBlueprint)

@app.route('/')
def index():
    return redirect(app.config["OPENAPI_SWAGGER_UI_PATH"])

if __name__ == '__main__':
    app.run(port=5555, debug=True)
