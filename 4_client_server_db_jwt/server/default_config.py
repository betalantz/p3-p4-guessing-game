"""Default application settings"""

import secrets
from datetime import timedelta


class DefaultConfig:
    """Default configuration"""

    API_TITLE = "Guessing Game API"
    API_VERSION = 0.1
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    PROPAGATE_EXCEPTIONS = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///gamedata.db"

    JWT_SECRET_KEY = str(secrets.SystemRandom().getrandbits(128))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=20)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_TOKEN_LOCATION = ["cookies"]
    # Storing the tokens in cookies protects agains XSS attacks but is vulnerable to CSRF attacks.
    # Best practice will be to set this to True, but it requires a CSRF token to be sent with every request.
    JWT_COOKIE_CSRF_PROTECT = False
