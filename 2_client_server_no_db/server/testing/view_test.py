import pytest
from app import app
from schemas import GameSchema


class TestGames:
    """
    The Games class in view.py

    """

    def test_games_get(self):
        """
        has a GET route for '/games'.
        """
        with app.test_client() as client:
            response = client.get("/games")
            assert response.status_code == 200
            assert response.json == []

    def test_games_post(self):
        """
        has a POST route for '/games'.
        """
        with app.test_client() as client:
            response = client.post(
                "/games", json={"difficulty": "easy", "range_min": 1, "range_max": 10}
            )
            assert response.status_code == 201
            assert ("difficulty", "easy") in response.json.items()
            assert ("range_min", 1) in response.json.items()
            assert ("range_max", 10) in response.json.items()
            assert ("is_over", False) in response.json.items()
            assert len(response.json["rounds"]) == 1
            next_response = client.get("/games")
            assert next_response.status_code == 200
            assert len(next_response.json) == 1
            assert next_response.json[0] == response.json

    def test_games_post_invalid_difficulty(self):
        """
        POST route for '/games' returns a 400 error if the difficulty is invalid.
        """
        with app.test_client() as client:
            response = client.post(
                "/games", json={"difficulty": "medium", "range_min": 1, "range_max": 10}
            )
            assert response.status_code == 422
            assert response.json["errors"]["json"] == {
                "difficulty": ["Must be one of: easy, hard."]
            }


class TestGamesById:
    """
    The GamesById class in view.py

    """

    def test_games_by_id_get(self, test_game):
        """
        has a GET route for '/games/<string:game_id>'.
        """
        with app.test_client() as client:
            response = client.get(f"/games/{test_game.id}")
            assert response.status_code == 200
            assert response.json == GameSchema().dump(test_game)

    def test_games_by_id_get_invalid_id(self):
        """
        GET route for '/games/<string:game_id>' returns a 404 error if the game id is invalid.
        """
        with app.test_client() as client:
            response = client.get("/games/invalid_id")
            assert response.status_code == 404
            assert response.json["message"] == "Game invalid_id not found."

    def test_games_by_id_patch(self, test_game):
        """
        has a PATCH route for '/games/<string:game_id>'.
        """
        with app.test_client() as client:
            response = client.patch(
                f"/games/{test_game.id}", json={"guess": test_game.secret_number}
            )
            assert response.status_code == 200
            assert response.json["is_over"] == True

    def test_games_by_id_patch_invalid_id(self):
        """
        PATCH route for '/games/<string:game_id>' returns a 404 error if the game id is invalid.
        """
        with app.test_client() as client:
            response = client.patch("/games/invalid_id", json={"guess": 1})
            assert response.status_code == 404
            assert response.json["message"] == "Game invalid_id not found."

    def test_games_by_id_patch_high_guess(self, test_game):
        """
        PATCH route for '/games/<string:game_id>' returns round status 'high' if the guess is too high.
        """
        with app.test_client() as client:
            response = client.patch(
                f"/games/{test_game.id}", json={"guess": test_game.secret_number + 1}
            )
            assert response.status_code == 200
            assert response.json["rounds"][-2]["status"] == "high"

    def test_games_by_id_patch_low_guess(self, test_game):
        """
        PATCH route for '/games/<string:game_id>' returns round status 'low' if the guess is too low.
        """
        with app.test_client() as client:
            response = client.patch(
                f"/games/{test_game.id}", json={"guess": test_game.secret_number - 1}
            )
            assert response.status_code == 200
            assert response.json["rounds"][-2]["status"] == "low"

    def test_games_by_id_delete(self, test_game):
        """
        has a DELETE route for '/games/<string:game_id>'.
        """
        with app.test_client() as client:
            response = client.delete(f"/games/{test_game.id}")
            assert response.status_code == 204
            assert response.data == b""
            next_response = client.get("/games")
            assert next_response.status_code == 200
            assert next_response.json == []
