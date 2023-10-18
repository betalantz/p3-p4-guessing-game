from app import api, app
from default_config import DefaultConfig
from flask_smorest import Api
from view import blp as GameBlueprint


class TestApp:
    """
    The App class in app.py
    """

    def test_app_config(self):
        """
        has a config attribute set to an instance of DefaultConfig.
        """
        assert app.config["API_TITLE"] == DefaultConfig.API_TITLE
        assert app.config["API_VERSION"] == DefaultConfig.API_VERSION
        assert app.config["OPENAPI_VERSION"] == DefaultConfig.OPENAPI_VERSION
        assert app.config["OPENAPI_URL_PREFIX"] == DefaultConfig.OPENAPI_URL_PREFIX
        assert (
            app.config["OPENAPI_SWAGGER_UI_PATH"]
            == DefaultConfig.OPENAPI_SWAGGER_UI_PATH
        )
        assert (
            app.config["OPENAPI_SWAGGER_UI_URL"] == DefaultConfig.OPENAPI_SWAGGER_UI_URL
        )
        assert app.config["PROPAGATE_EXCEPTIONS"] == DefaultConfig.PROPAGATE_EXCEPTIONS
        assert app.config["DEBUG"] == DefaultConfig.DEBUG

    def test_app_json_compact(self):
        """
        has a json.compact attribute set to False.
        """
        assert app.json.compact is False

    def test_app_api(self):
        """
        has an api attribute set to an instance of Api.
        """
        assert isinstance(api, Api)

    def test_app_index(self):
        """
        has an index route that redirects to the swagger ui.
        """
        with app.test_client() as client:
            response = client.get("/")
            assert response.status_code == 302
            assert response.headers["Location"] == "/swagger-ui"

    def test_game_blueprint_get(self):
        """
        GameBlueprint has a GET route for '/games'.
        """
        with app.test_client() as client:
            response = client.get("/games")
            assert response.status_code not in range(400, 599)
