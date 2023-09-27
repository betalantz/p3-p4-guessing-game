from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    jwt_required,
)
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select

from db import db
from models import User
from schemas import UserSchema
from blocklist import BLOCKLIST

blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/register")
class UsersRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        #if User.query.filter(User.name == user_data["name"]).first():
        user =  db.session.scalars(select(User).where(User.name == user_data["name"])).first()
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
        #user = User.query.filter(
        #    User.username == user_data["username"]
        #).first()
        user =  db.session.scalars(select(User).where(User.name == user_data["name"])).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200

        abort(401, message="Invalid credentials.")
        
@blp.route("/logout")
class UsersLogout(MethodView):
    @jwt_required()
    @blp.doc(authorize=True)
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200