from db import db
from passlib.hash import pbkdf2_sha256
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    _password_hash = db.Column(db.String(255), nullable=False)

    @hybrid_property
    def password(self):
        return self._password_hash

    # move password hashing to model so seeded user passwords will be hashed
    @password.setter
    def password(self, password):
        self._password_hash = pbkdf2_sha256.hash(password)

    # also authenticate on model so hashing library is not imported in resource
    def authenticate(self, password):
        return pbkdf2_sha256.verify(password, self._password_hash)

    games = db.relationship("Game", back_populates="user", cascade="all, delete-orphan")
