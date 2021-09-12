from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from utils.exceptions import DatabaseException, UserNotExistingException, UsernameDuplicateException
from entities.user import User
from utils.database import db


class UserRepository:
    """Class used for handling users in the database
    """

    def new(self, username: str, user_role: int, password_hash: str, firstname: str, lastname: str, email: str) -> User:
        """new is used to create new users into the database.

        Args:
            username (str): user's unique username
            user_role (int): user's role in the application
            password_hash (str): user's password in encrypted format
            firstname (str): user's firstname
            lastname (str): user's lastname
            email (str): user's email address

        Raises:
            DatabaseException: raised if problems while saving into database.
            UsernameDuplicateException: raised if given username is already in use.

        Returns:
            User: created user as User object
        """
        values = {
            "username": username,
            "user_role": user_role,
            "password_hash": password_hash,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "profile_image": "default"
        }
        sql = """INSERT INTO Users
                (username, user_role, password_hash, 
                firstname, lastname, email) 
                VALUES (:username, :user_role, :password_hash, 
                :firstname, :lastname, :email) 
                RETURNING id"""
        try:
            uid = db.session.execute(sql, values).fetchone()[0]
            db.session.commit()
        except IntegrityError as error:
            raise UsernameDuplicateException() from error
        except Exception as error:
            print(error)
            raise DatabaseException(
                'While saving new user into database') from error
        if not uid:
            raise DatabaseException('While saving new user into database')

        created_user = User(uid, username, user_role, password_hash,
                            firstname, lastname, email, values["profile_image"])
        return created_user

    def get_by_id(self, uid: str) -> User:
        """get_by_id is used to get user with given id

        Args:
            id (str): id of user in search

        Raises:
            UserNotExistingException: raised if user not found with given id
            DatabaseException: if problem occurs while handling with database

        Returns:
            User: found user as User object
        """
        sql = "SELECT * FROM Users WHERE id=:id"
        try:
            result = db.session.execute(sql, {"id": uid})
            user = result.fetchone()
        except Exception as error:
            raise DatabaseException(
                'while getting user by username') from error

        if not user:
            raise UserNotExistingException()

        return User(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7])

    def get_by_username(self, username: str) -> User:
        """get_by_username is used to get user with given username

        Args:
            username (str): username of user in search

        Raises:
            UserNotExistingException: raised if user not found with given username
            DatabaseException: if problem occurs while handling with database

        Returns:
            User: found user as User object
        """
        sql = "SELECT * FROM Users WHERE username=:username"
        try:
            result = db.session.execute(sql, {"username": username.lower()})
            user = result.fetchone()
        except Exception as error:
            raise DatabaseException(
                'while getting user by username') from error

        if not user:
            raise UserNotExistingException()

        return User(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7])

    def update(self, uid: str, username: str, user_role: int, password_hash: str, firstname: str, lastname: str, email: str, profile_image: str) -> User:
        """update is used to change values of user into database

        Args:
            uid (str): id of user
            username (str): user's username, needs to be unique
            user_role (int): user's user_role
            password_hash (str): user's password as encrypted hash
            firstname (str): user's firstname
            lastname (str): user's lastname
            email (str): user's email
            profile_image (str): user's profile_image

        Raises:
            DatabaseException: raised if problems while saving into database
            UsernameDuplicateException: raised if given username is already in use.

        Returns:
            User: user object with updated values
        """
        values = {
            "username": username,
            "user_role": user_role,
            "password_hash": password_hash,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "profile_image": profile_image,
            "id": uid
        }
        sql = "UPDATE Users SET username=:username, user_role=:user_role, password_hash=:password_hash, name=:name, email=:email, profile_image=:profile_image WHERE id=:id"
        try:
            db.session.execute(sql, values)
            db.session.commit()
        except IntegrityError as error:
            raise UsernameDuplicateException() from error
        except Exception as error:
            raise DatabaseException('user update') from error
        return User(uid, username, user_role, password_hash, firstname, lastname, email, profile_image)

    def remove(self, uid: str):
        """remove is used to remove user's from database

        Args:
            uid (str): id of user to be removed

        Raises:
            UserNotExistingException: raised if user not found with given id
            DatabaseException: raised if problems while interacting with database
        """
        if not self.get_by_id(uid):
            raise UserNotExistingException()
        sql = "DELETE FROM Users WHERE id=:id"
        try:
            db.session.execute(sql, {"id": uid})
            db.session.commit()
        except Exception as error:
            print(error)
            raise DatabaseException('user remove') from error


user_repository = UserRepository()
