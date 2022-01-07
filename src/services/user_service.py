from werkzeug.security import generate_password_hash, check_password_hash

from entities.user import User

from repositories.user_repository import user_repository, UserRepository
from repositories.team_repository import team_repository, TeamRepository

from services.role_service import role_service, RoleService

from utils.helpers import image_string, fullname
from utils.validators import validate_uuid4
from utils.exceptions import ValueShorterThanException, EmptyValueException, LoginException, NotExistingException, UnvalidInputException


class UserService:
    '''Class used for handling users in the application
    '''

    def __init__(self,
                 default_user_repository: UserRepository = user_repository,
                 default_team_repository: TeamRepository = team_repository,
                 default_role_service: RoleService = role_service):
        '''Initializes UserService with default user repository

        Args:
            default_user_repository (UserRepository, optional):
                interaction module with database for users.
                Defaults to user_repository.
            default_role_service (RoleService, optional):
                interaction module with roles.
                Defaults to role_service.
        '''
        self._user_repository = default_user_repository
        self._team_repository = default_team_repository
        self._role_service = default_role_service

    def new(self, username: str, user_role: str, password: str, firstname: str,
            lastname: str, email: str) -> User:
        '''new is used to create new users

        Args:
            username (str): user's unique username
            user_role (str): user's role in the application
            password (str): user's password as not encrypted version,
                used to create encrypted hash
            firstname (str): user's firstname
            lastname (str): user's lastname
            email (str): user's email

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database
            UnvalidInputException: raised if email is
                given in unvalid format.
            UsernameDuplicateException: raised if given
                username is already in use.
            ValueShorterThanException: raised if username or password are
                not longer than 5 characters
            EmptyValueException: raised if username, password, firstname
                or lastname are empty

        Returns:
            User: created user
        '''
        if len(username) > 100 or len(password) > 100 or len(
                firstname) > 100 or len(lastname) > 100 or len(email) > 100:
            raise UnvalidInputException('Input values too long')

        if username == '':
            raise EmptyValueException('username')
        elif len(username) < 5:
            raise ValueShorterThanException('username', 5)

        if password == '':
            raise EmptyValueException('password')
        elif len(password) < 5:
            raise ValueShorterThanException('password', 5)

        if firstname == '' or lastname == '':
            raise EmptyValueException('name')

        username = username.lower()

        try:
            user_role = int(user_role)
        except Exception as error:
            raise UnvalidInputException('Unvalid input', 'unexpected value',
                                        'user role') from error

        password_hash = generate_password_hash(password)

        user_role_name = self._role_service.get_by_id(user_role)
        if not user_role_name:
            raise NotExistingException('Role')

        user_id = self._user_repository.new(username, user_role, password_hash,
                                            firstname, lastname, email)

        created_user = User(user_id, username, user_role, user_role_name,
                            password_hash, firstname, lastname, email)

        return created_user

    def get_by_id(self, uid: str) -> User:
        '''get_by_id is used to found user with given id

        Args:
            uid (str): id of the user

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if there is none users with given id
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            User: found user
        '''

        if not validate_uuid4(uid):
            raise UnvalidInputException("User's id")

        user = self._user_repository.get_by_id(uid)
        return User(user[0], user[1], user[2], user[3],
                    user[4], user[5], user[6], user[7],
                    image_string(user[8], user[9]), user[10], user[11])

    def get_by_username(self, username: str) -> User:
        '''get_by_username is used to find users from database by username

        Args:
            username (str): username of user to be found

        Raises:
            UserNotExistingException: raised if user not found
                with given username
            DatabaseException: if problem occurs while handling with database

        Returns:
            User: found user
        '''

        user = self._user_repository.get_by_username(username)
        return User(user[0], user[1], user[2], user[3],
                    user[4], user[5], user[6], user[7],
                    image_string(user[8], user[9]), user[10], user[11])

    def get_all(self) -> [User]:
        '''get_all is used to list of all users in the database

        If no users found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [User]: list of all users
        '''

        users = [
            User(user[0], user[1], user[2], user[3], user[4], user[5], user[6],
                 user[7], image_string(user[8], user[9]), user[10], user[11])
            for user in self._user_repository.get_all()
        ]
        return users

    def get_all_by_team(self, teid: str) -> [User]:
        '''get_all is used to list of all features in the database

        If no features found, returns empty list.

        Args:
            teid (str): id of the team

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if team with given
                id not found
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            [tuple]: list of all features
        '''

        if not validate_uuid4(teid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='Team ID')

        if not self._team_repository.get_by_id(teid):
            raise NotExistingException('Team')

        users = [
            User(user[0], user[1], user[2], user[3], user[4], user[5], user[6],
                 user[7], image_string(user[8], user[9]), user[10], user[11])
            for user in self._user_repository.get_all_by_team(teid)
        ]
        return users

    def get_users(self) -> [tuple]:
        '''get_users is used to get all users for
           selecting users in the frontend

        If no users found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of users id, name and profile image
        '''

        users = [(user[0], fullname(user[1],
                                    user[2]), image_string(user[3], user[4]))
                 for user in self._user_repository.get_users()]
        return users

    def get_team_users(self, teid: str) -> [tuple]:
        '''get_team_users is used to get all users for
           selecting users in the frontend

        If no users found, returns empty list.

        Args:
            teid (str): id of the team

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if team with given
                id not found
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            [tuple]: list of users, name and profile image
        '''
        if not validate_uuid4(teid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='Team ID')

        if not self._team_repository.get_by_id(teid):
            raise NotExistingException('Team')

        users = [(user[0], fullname(user[1],
                                    user[2]), image_string(user[3], user[4]))
                 for user in self._user_repository.get_team_users(teid)]
        return users

    def get_fullname(self, uid: str) -> str:
        '''get_fullname is used to get name of user with given id

        Args:
            uid (str): id of the user

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if user is not
                found with given id
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            str: found name
        '''

        if not validate_uuid4(uid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='User ID')

        if not self._user_repository.get_by_id(uid):
            raise NotExistingException('User')

        name = self._user_repository.get_fullname(uid)
        return fullname(name[0], name[1])

    def get_profile_image(self, uid: str) -> str:
        '''get_profile_image is used to get profile image
           of user with given id

        Args:
            uid (str): id of the user

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if user is not
                found with given id
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            str: found profile image
        '''
        if not validate_uuid4(uid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='User ID')

        if not self._user_repository.get_by_id(uid):
            raise NotExistingException('User')

        image = self._user_repository.get_profile_image(uid)
        return image_string(image[0], image[1])

    def update_profile_image(self, uid: str, img_type: str, img_data: str):
        """update_profile_image is used to update user's
           profile images into the database

        Args:
            uid (str): uid (str): id of user
            img_type (str): type of the image.
            img_data (str): byte data of the image

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database
            UnvalidInputException: raised if unvalid
                id or mage is given
            NotExistingException: raised if user is not
                found with given id
        """
        if not validate_uuid4(uid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='User ID')

        if not self._user_repository.get_by_id(uid):
            raise NotExistingException('User')

        if img_type not in ['image/jpeg', 'image/png', 'image/gif']:
            raise UnvalidInputException('''Profile image type not supported,
                supported types are "image/jpeg", "image/png", "image/gif"''')

        if len(img_data) > 1000 * 1024:
            raise UnvalidInputException(
                'Profile image size too big, supports only < 1MB')

        return self._user_repository.update_profile_image(
            uid, img_type, img_data)

    def update(self, uid: str, username: str, user_role: str, password: str,
               firstname: str, lastname: str, email: str) -> User:
        '''update is used to update users

        Args:
            uid (str): id of user to be updated
            username (str): user's username, needs to be unique
            user_role (str): user's user role
            password (str): user's password as not encrypted
                version, used to create encrypted hash
            firstname (str): user's firstname
            lastname (str): user's lastname
            email (str): user's email
            profile_image (str): user's profile image as base64 encoded

        Raises:
            ValueShorterThanException: raised if username or
                password are not longer than 5 characters
            EmptyValueException: raised if username, password,
                firstname or lastname are empty
            DatabaseException: raised if problems occurs while
                saving into the database
            UsernameDuplicateException: raised if given username
                is already in use.
            UnvalidInputException: raised if formatting of given
                input value is incorrect

        Returns:
            User: updated user as user object
        '''
        if len(username) > 100 or len(password) > 100 or len(
                firstname) > 100 or len(lastname) > 100 or len(email) > 100:
            raise UnvalidInputException('Input values too long')

        if not validate_uuid4(uid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='User ID')

        current_user = self.get_by_id(uid)
        if not current_user:
            raise NotExistingException('User')

        if username == '':
            raise EmptyValueException('username')
        elif len(username) < 5:
            raise ValueShorterThanException('username', 5)

        if password == '':
            raise EmptyValueException('password')
        elif len(password) < 5:
            raise ValueShorterThanException('password', 5)

        if firstname == '' or lastname == '':
            raise EmptyValueException('name')

        username = username.lower()

        try:
            user_role = int(user_role)
        except Exception as error:
            raise UnvalidInputException('Unvalid input', 'unexpected value',
                                        'user role') from error

        password_hash = generate_password_hash(password)

        user_role_name = self._role_service.get_by_id(user_role)
        if not user_role_name:
            raise NotExistingException('Role')

        user_id = self._user_repository.new(username, user_role, password_hash,
                                            firstname, lastname, email)

        updated_user = User(user_id, username, user_role, user_role_name,
                            password_hash, firstname, lastname, email)

        return updated_user

    def remove(self, uid: str):
        '''remove is used to remove user

        Args:
            uid (str): id of user to be removed

        Raises:
            DatabaseException: raised if problems occurs
                while interacting with database.
            NotExistingException: raised if user not found with given id
            UnvalidInputException: raised if unvalid
                id is given
        '''

        if not validate_uuid4(uid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='feature id')

        self._user_repository.get_by_id(uid)
        self._user_repository.remove(uid)

    def login(self, username: str, password: str) -> str:
        '''login is used to check if given username and password are valid

        Args:
            username (str): username to be checked
            password (str): password to be checked

        Raises:
            LoginException: raised if username or password are incorrect

        Returns:
            str: user id for session
        '''
        try:
            user = self.get_by_username(username)
        except NotExistingException as error:
            raise LoginException() from error
        if check_password_hash(user.password_hash, password):
            return (user.user_id, user.fullname, user.user_role, user.team_id)
        raise LoginException()


user_service = UserService()
