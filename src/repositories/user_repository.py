import re
from sqlalchemy import exc
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from utils.exceptions import DatabaseException, UnvalidInputException, NotExistingException, UsernameDuplicateException
from entities.user import User
from utils.database import db
from utils.helpers import fullname


class UserRepository:
    """Class used for handling users in the database
    """

    def new(self, username: str, user_role: int, password_hash: str,
            firstname: str, lastname: str, email: str) -> User:
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
            UnvalidInputException: raised if email is given in unvalid format.
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
            unvalid_email = re.compile(r'.*"users_email_check".*')
            duplicate_username = re.compile(
                r'.*duplicate key value violates unique constraint "users_username_key".*'
            )
            if unvalid_email.match(str(error)):
                raise UnvalidInputException("Unvalid input",
                                            "unvalid formatting",
                                            "email") from error
            elif duplicate_username.match(str(error)):
                raise UsernameDuplicateException() from error
            else:
                raise DatabaseException(
                    'While saving new user into database') from error
        except Exception as error:
            raise DatabaseException(
                'While saving new user into database') from error
        if not uid:
            raise DatabaseException('While saving new user into database')

        created_user = User(uid, username, user_role, password_hash, firstname,
                            lastname, email, values["profile_image"])
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
            raise DatabaseException('while getting user by username') from error

        if not user:
            raise NotExistingException('User')

        return User(user[0], user[1], user[2], user[3], user[4], user[5],
                    user[6], user[7])

    def get_by_username(self, username: str) -> User:
        """get_by_username is used to get user with given username

        Args:
            username (str): username of user in search

        Raises:
            NotExistingException: raised if user not found with given username
            DatabaseException: if problem occurs while handling with database

        Returns:
            User: found user as User object
        """
        sql = "SELECT * FROM Users WHERE username=:username"
        try:
            result = db.session.execute(sql, {"username": username.lower()})
            user = result.fetchone()
        except Exception as error:
            raise DatabaseException('while getting user by username') from error

        if not user:
            raise NotExistingException('User')

        return User(user[0], user[1], user[2], user[3], user[4], user[5],
                    user[6], user[7])

    def get_fullname(self, uid: str) -> str:
        sql = "SELECT firstname, lastname FROM Users WHERE id=:id"
        try:
            firstname, lastname = db.session.execute(sql, {
                "id": uid
            }).fetchone()
        except Exception as error:
            raise DatabaseException('while getting user´s fullname') from error
        if not firstname or not lastname:
            raise NotExistingException('User')
        return fullname(firstname, lastname)

    def get_all(self) -> list[User]:
        """get_all is used to get all users in the database

        Raises:
            DatabaseException: if problem occurs while handling with database

        Returns:
            list[User]: list of all users
        """
        sql = "SELECT * FROM Users"
        try:
            result = db.session.execute(sql)
            users = result.fetchall()
        except Exception as error:
            raise DatabaseException('while getting all users') from error

        return [
            User(user[0], user[1], user[2], user[3], user[4], user[5], user[6],
                 user[7]) for user in users
        ]

    def get_users(self) -> list[tuple]:
        """get_users is used to get all users for selecting users in the frontend

        Raises:
            DatabaseException: if problem occurs while handling with database

        Returns:
            list[tuple]: list of users id and fullname
        """
        sql = "SELECT id, firstname, lastname FROM Users"
        try:
            users = db.session.execute(sql).fetchall()
        except Exception as error:
            raise DatabaseException('while getting all users') from error

        return [(user[0], fullname(user[1], user[2])) for user in users]

    def update(self, uid: str, username: str, user_role: int,
               password_hash: str, firstname: str, lastname: str, email: str,
               profile_image: str) -> User:
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
        sql = "UPDATE Users SET username=:username, user_role=:user_role, password_hash=:password_hash, firstname=:firstname, lastname=:lastname, email=:email, profile_image=:profile_image WHERE id=:id"
        try:
            db.session.execute(sql, values)
            db.session.commit()
        except IntegrityError as error:
            raise UsernameDuplicateException() from error
        except Exception as error:
            raise DatabaseException('user update') from error
        return User(uid, username, user_role, password_hash, firstname,
                    lastname, email, profile_image)

    def remove(self, uid: str):
        """remove is used to remove user's from database

        Args:
            uid (str): id of user to be removed

        Raises:
            NotExistingException: raised if user not found with given id
            DatabaseException: raised if problems while interacting with database
        """
        if not self.get_by_id(uid):
            raise NotExistingException('User')
        sql = "DELETE FROM Users WHERE id=:id"
        try:
            db.session.execute(sql, {"id": uid})
            db.session.commit()
        except Exception as error:
            raise DatabaseException('user remove') from error


user_repository = UserRepository()
