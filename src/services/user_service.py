from werkzeug.security import generate_password_hash, check_password_hash
from utils.exceptions import ValueShorterThanException, EmptyValueException, LoginException, UserNotExistingException, UnvalidInputException
from entities.user import User
from utils.database import db
from repositories.user_repository import user_repository, UserRepository


class UserService:
    """Class used for handling users in the application
    """

    def __init__(self, default_user_repository: UserRepository = user_repository):
        """Initializes UserService with default user repository

        Args:
            default_user_repository (UserRepository, optional): option to give custom user_repository. Defaults to user_repository.
        """
        self._user_repository = default_user_repository

    def new(self, username: str, user_role: str, password: str, firstname: str, lastname: str, email: str) -> User:
        """new is used to create new users

        Args:
            username (str): user's username, needs to be unique
            user_role (str): user's user role as integer format, inputted as string, 1 = lowest permission level
            password (str): user's password as not encrypted version, used to create encrypted hash
            firstname (str): user's firstname
            lastname (str): user's lastname
            email (str): user's email

        Raises:
            ValueShorterThanException: raised if username or password are not longer than 5 characters
            EmptyValueException: raised if username, password, firstname or lastname are empty
            DatabaseException: raised if problems while saving into database.
            UsernameDuplicateException: raised if given username is already in use

        Returns:
            User: created user as user object
        """
        if username == "":
            raise EmptyValueException('username')
        elif len(username) < 5:
            raise ValueShorterThanException('username', 5)

        if password == "":
            raise EmptyValueException('password')
        elif len(password) < 5:
            raise ValueShorterThanException('password', 5)

        if firstname == "" or lastname == "":
            raise EmptyValueException('name')

        username = username.lower()
        try:
            user_role = int(user_role)
        except Exception as error:
            raise UnvalidInputException(
                "Unvalid input", "unexpected value", "user role") from error
        password_hash = generate_password_hash(password)

        created_user = self._user_repository.new(
            username, user_role, password_hash, firstname, lastname, email)
        return created_user

    def get_by_id(self, uid: str) -> User:
        """get_by_id is used to find user's from databse by id

        Args:
            uid (str): id of user to be found

        Raises:
            UserNotExistingException: raised if user not found with given id

        Returns:
            User: found user
        """
        user = self._user_repository.get_by_id(uid)
        return user

    def get_by_username(self, username: str) -> User:
        """get_by_username is used to find users from database by username

        Args:
            username (str): username of user to be found

        Raises:
            UserNotExistingException: raised if user not found with given username
            DatabaseException: if problem occurs while handling with database

        Returns:
            User: found user
        """
        user = self._user_repository.get_by_username(username)
        return user

    def get_all(self) -> list[User]:
        """get_all is used to get all users in the database

        Raises:
            DatabaseException: if problem occurs while handling with database

        Returns:
            list[User]: list of all users in the database
        """
        users = self._user_repository.get_all()
        return users

    def update(self, uid: str, username: str, user_role: str, password: str, firstname: str, lastname: str, email: str, profile_image: str) -> User:
        """update is used to update users

        Args:
            uid (str): id of user to be updated
            username (str): user's username, needs to be unique
            user_role (str): user's user role
            password (str): user's password as not encrypted version, used to create encrypted hash
            firstname (str): user's firstname
            lastname (str): user's lastname
            email (str): user's email
            profile_image (str): user's profile image as base64 encoded

        Raises:
            ValueShorterThanException: raised if username or password are not longer than 5 characters
            EmptyValueException: raised if username, password, firstname or lastname are empty
            DatabaseException: raised if problems while saving into database.
            UsernameDuplicateException: raised if given username is already in use

        Returns:
            User: updated user as user object
        """
        current_user = self.get_by_id(uid)

        if username == "":
            raise EmptyValueException('username')
        elif len(username) < 5:
            raise ValueShorterThanException('username', 5)

        if password == "":
            raise EmptyValueException('password')
        elif len(password) < 5:
            raise ValueShorterThanException('password', 5)

        if firstname == "" or lastname == "":
            raise EmptyValueException('name')

        if user_role != str(current_user.user_role):
            try:
                user_role = int(user_role)
            except Exception as error:
                raise UnvalidInputException(
                    "Unvalid input", "unexpected value", "user role") from error

        username = current_user.username if username == current_user.username else username.lower()
        password_hash = current_user.password_hash if password == "" else generate_password_hash(
            password)
        profile_image = profile_image if profile_image != "" else "default_image"

        user = self._user_repository.update(
            uid, username, user_role, password_hash, firstname, lastname, email, profile_image)

        return user

    def remove(self, uid: str):
        """remove is used to remove user's from database

        Args:
            uid (str): id of user to be removed

        Raises:
            UserNotExistingException: raised if user not found with given id
            DatabaseException: raised if problems while interacting with database
        """
        self._user_repository.remove(uid)

    def login(self, username: str, password: str) -> str:
        """login is used to check if given username and password are valid

        Args:
            username (str): username to be checked
            password (str): password to be checked

        Raises:
            LoginException: raised if username or password are incorrect

        Returns:
            str: user id for session
        """
        try:
            user = self.get_by_username(username)
        except UserNotExistingException as usernotfound:
            raise LoginException() from usernotfound
        if check_password_hash(user.password_hash, password):
            return user.user_id
        raise LoginException()


user_service = UserService()
