from typing import Union
from entities.user import User
from db import db


class UserRepository:

    def new(self, username: str, user_role: int, password_hash: str,
            firstname: str, lastname: str, email: str, profile_image: str) -> User:
        sql = "INSERT INTO Users (username, user_role, password_hash, firstname, lastname, email, "
        sql += "profile_image) VALUES (:username, :user_role, :password_hash, :firstname, "
        sql += " :lastname, :email, :profile_image) RETURNING id"

        values = {
            "username": username,
            "user_role": user_role,
            "password_hash": password_hash,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "profile_image": profile_image,
        }

        result = db.session.execute(sql, values)
        db.session.commit()
        user_id = str(result.fetchone()[0])

        user = User(user_id, username, user_role, password_hash,
                    firstname, lastname, email, profile_image)
        return user

    def find_username(self, username) -> Union[User, None]:
        sql = "SELECT * FROM Users WHERE username=:username"
        result = db.session.execute(sql, {"username": username})
        print(result.fetchone())


user_repository = UserRepository()
