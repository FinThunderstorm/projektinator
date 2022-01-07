import re
from sqlalchemy.exc import IntegrityError
from utils.exceptions import DatabaseException, UnvalidInputException, NotExistingException, UsernameDuplicateException
from utils.database import db


class UserRepository:
    '''Class used for handling users in the database
    '''

    def new(self, username: str, user_role: int, password_hash: str,
            firstname: str, lastname: str, email: str) -> str:
        '''new is used to create new users into the database.

        Args:
            username (str): user´s unique username
            user_role (int): user´s role in the application
            password_hash (str): user´s password in encrypted format
            firstname (str): user´s firstname
            lastname (str): user´s lastname
            email (str): user´s email address

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database
            UnvalidInputException: raised if email is
                given in unvalid format.
            UsernameDuplicateException: raised if given
                username is already in use.

        Returns:
            tuple: created user´s id'
        '''

        values = {
            'username': username,
            'user_role': user_role,
            'password_hash': password_hash,
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
        }

        sql = '''
            INSERT INTO Users
            (username, user_role, password_hash, 
            firstname, lastname, email) 
            VALUES (:username, :user_role, :password_hash, 
            :firstname, :lastname, :email) 
            RETURNING id
        '''

        try:
            user_id = db.session.execute(sql, values).fetchone()[0]
            db.session.commit()
        except IntegrityError as error:
            unvalid_email = re.compile(r'.*"users_email_check".*')
            duplicate_username = re.compile(
                r'.*violates unique constraint "users_username_key".*')

            if unvalid_email.match(str(error)):
                raise UnvalidInputException('Unvalid input',
                                            'unvalid formatting',
                                            'email') from error
            elif duplicate_username.match(str(error)):
                raise UsernameDuplicateException() from error
            else:
                raise DatabaseException('While saving new user') from error

        except Exception as error:
            raise DatabaseException(
                'While saving new user into database') from error

        if not user_id:
            raise DatabaseException('While saving new user into database')

        return user_id

    def get_by_id(self, uid: str) -> tuple:
        '''get_by_id is used to found user with given id

        Args:
            uid (str): id of the user

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if there is none users with given id

        Returns:
            tuple: found user
        '''

        sql = '''
            SELECT U.id, U.username, U.user_role, R.name, U.password_hash, U.firstname, U.lastname, U.email, PI.image_type, encode(PI.image_data, 'base64'), T.id, T.name 
            FROM Users U
            LEFT JOIN Teamsusers TU ON U.id = TU.user_id
            LEFT JOIN Teams T ON TU.team_id = T.id
            LEFT JOIN ProfileImages PI ON PI.user_id = U.id
            LEFT JOIN Roles R ON R.id = U.user_role
            WHERE U.id=:id
        '''

        try:
            user = db.session.execute(sql, {'id': uid}).fetchone()
        except Exception as error:
            raise DatabaseException('While getting user by id') from error

        if not user:
            raise NotExistingException('User')

        return (user[0], user[1], user[2], user[3], user[4], user[5], user[6],
                user[7], user[8], user[9], user[10], user[11])

    def get_by_username(self, username: str) -> tuple:
        '''get_by_id is used to found user with given username

        Args:
            username (str): username of the user

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if there is none user with given id

        Returns:
            tuple: found user
        '''

        sql = '''
            SELECT U.id, U.username, U.user_role, R.name, U.password_hash, U.firstname, U.lastname, U.email, PI.image_type, encode(PI.image_data, 'base64'), T.id, T.name 
            FROM Users U
            LEFT JOIN Teamsusers TU ON U.id = TU.user_id
            LEFT JOIN Teams T ON TU.team_id = T.id
            LEFT JOIN ProfileImages PI ON PI.user_id = U.id
            LEFT JOIN Roles R ON R.id = U.user_role
            WHERE U.username=:username
        '''

        values = {'username': username.lower()}

        try:
            user = db.session.execute(sql, values).fetchone()
        except Exception as error:
            raise DatabaseException('While getting user by username') from error

        if not user:
            raise NotExistingException('User')

        return (user[0], user[1], user[2], user[3], user[4], user[5], user[6],
                user[7], user[8], user[9], user[10], user[11])

    def get_fullname(self, uid: str) -> tuple:
        '''get_fullname is used to get name of user with given id

        Args:
            uid (str): id of the user

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if user is not
                found with given id

        Returns:
            tuple: found name
        '''

        sql = '''
            SELECT firstname, lastname 
            FROM Users 
            WHERE id=:id
        '''

        try:
            firstname, lastname = db.session.execute(sql, {
                'id': uid
            }).fetchone()
        except Exception as error:
            raise DatabaseException('While getting user´s fullname') from error

        if not firstname or not lastname:
            raise NotExistingException('User')

        return (firstname, lastname)

    def get_profile_image(self, uid: str) -> tuple:
        '''get_profile_image is used to get profile image
           of user with given id

        Args:
            uid (str): id of the user

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            tuple: found profile image
        '''

        sql = '''
            SELECT U.id, PI.image_type, encode(PI.image_data, 'base64') 
            FROM Users U
            LEFT JOIN ProfileImages PI ON PI.user_id = U.id
            WHERE U.id=:id
        '''

        try:
            user_id, image_type, image_data = db.session.execute(
                sql, {
                    'id': uid
                }).fetchone()
        except Exception as error:
            raise DatabaseException(
                'While getting user´s profile image') from error

        if str(user_id) != str(uid):
            raise DatabaseException('')

        return (image_type, image_data)

    def get_all(self) -> [tuple]:
        '''get_all is used to list of all users in the database

        If no users found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of all users
        '''

        sql = '''
            SELECT U.id, U.username, U.user_role, R.name, U.password_hash, U.firstname, U.lastname, U.email, PI.image_type, encode(PI.image_data, 'base64'), T.id, T.name 
            FROM Users U
            LEFT JOIN Teamsusers TU ON U.id = TU.user_id
            LEFT JOIN Teams T ON TU.team_id = T.id
            LEFT JOIN ProfileImages PI ON PI.user_id = U.id
            LEFT JOIN Roles R ON R.id = U.user_role
        '''

        try:
            result = db.session.execute(sql)
            users = result.fetchall()
        except Exception as error:
            raise DatabaseException('While getting all users') from error

        return [(user[0], user[1], user[2], user[3], user[4], user[5], user[6],
                 user[7], user[8], user[9], user[10], user[11])
                for user in users]

    def get_all_by_team(self, teid: str) -> [tuple]:
        '''get_all_by_team is used to list of all users in the database
           with given team id

        If no users found, returns empty list.

        Args:
            teid (str): id of the team

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of all users
        '''

        sql = '''
            SELECT U.id, U.username, U.user_role, R.name, U.password_hash, U.firstname, U.lastname, U.email, PI.image_type, encode(PI.image_data, 'base64'), T.id, T.name 
            FROM Users U
            LEFT JOIN Teamsusers TU ON U.id = TU.user_id
            LEFT JOIN Teams T ON TU.team_id = T.id
            LEFT JOIN ProfileImages PI ON PI.user_id = U.id
            LEFT JOIN Roles R ON R.id = U.user_role
            WHERE TU.team_id=:id
        '''

        try:
            users = db.session.execute(sql, {'id': teid}).fetchall()
        except Exception as error:
            raise DatabaseException(
                'While getting all users by team') from error

        return [(user[0], user[1], user[2], user[3], user[4], user[5], user[6],
                 user[7], user[8], user[9], user[10], user[11])
                for user in users]

    def get_users(self) -> [tuple]:
        '''get_users is used to get all users for
           selecting users in the frontend

        If no users found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of user id, name and profile images
        '''

        sql = '''
            SELECT U.id, U.firstname, U.lastname, PI.image_type, encode(PI.image_data, 'base64')
            FROM Users U
            LEFT JOIN ProfileImages PI ON PI.user_id = U.id
        '''

        try:
            users = db.session.execute(sql).fetchall()
        except Exception as error:
            raise DatabaseException('While getting all users') from error

        return [(user[0], user[1], user[2], user[3], user[4]) for user in users]

    def get_team_users(self, teid: str) -> [tuple]:
        '''get_team_users is used to get all team´s users for
           selecting users in the frontend

        If no users found, returns empty list.

        Args:
            teid (str): id of the team

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of user id, name and profile images
        '''

        sql = '''
            SELECT U.id, U.firstname, U.lastname, PI.image_type, encode(PI.image_data, 'base64')
            FROM Users U
            LEFT JOIN Teamsusers TU ON TU.user_id = U.id
            LEFT JOIN ProfileImages PI ON PI.user_id = U.id
            WHERE TU.team_id=:id
        '''

        try:
            users = db.session.execute(sql, {'id': teid}).fetchall()
        except Exception as error:
            raise DatabaseException('While getting all users') from error

        return [(user[0], user[1], user[2], user[3], user[4]) for user in users]

    def update_profile_image(self, uid: str, img_type: str,
                             img_data: str) -> str:
        '''update_profile_image is used to update user´s
           profile images into the database

        Args:
            uid (str): uid (str): id of user
            img_type (str): type of the image.
            img_data (str): byte data of the image

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database
        '''

        sql = '''
            INSERT INTO ProfileImages
            (user_id, image_type, image_data)
            VALUES (:user_id, :image_type, :image_data)
            ON CONFLICT (user_id) DO UPDATE
                SET image_type = excluded.image_type,
                    image_data = excluded.image_data
            RETURNING user_id
        '''

        values = {
            'user_id': uid,
            'image_type': img_type,
            'image_data': img_data
        }

        try:
            db.session.execute(sql, values)
            db.session.commit()
        except Exception as error:
            raise DatabaseException('While updating profile image') from error

    def update(self, uid: str, username: str, user_role: int,
               password_hash: str, firstname: str, lastname: str,
               email: str) -> str:
        '''update is used to update feature with given values into the database

        Args:
            uid (str): id of the user
            username (str): user´s unique username
            user_role (int): user´s role in the application
            password_hash (str): user´s password in encrypted format
            firstname (str): user´s firstname
            lastname (str): user´s lastname
            email (str): user´s email address

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database
            UsernameDuplicateException: raised if given username
                is already in use.

        Returns:
            str: user´s id
        '''

        values = {
            'username': username,
            'user_role': user_role,
            'password_hash': password_hash,
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'id': uid
        }

        sql = '''
            UPDATE Users 
            SET username=:username, user_role=:user_role, password_hash=:password_hash, 
            firstname=:firstname, lastname=:lastname, email=:email
            WHERE id=:id
            RETURNING id
        '''

        try:
            user_id = db.session.execute(sql, values).fetchone()
            db.session.commit()
        except IntegrityError as error:
            raise UsernameDuplicateException() from error
        except Exception as error:
            raise DatabaseException('user update') from error

        return user_id[0]

    def remove(self, uid: str):
        '''remove is used to remove feature from the database

        Args:
            fid (str): id of the feature to be removed

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
        '''

        sql = '''
            DELETE FROM Users 
            WHERE id=:id
        '''

        try:
            db.session.execute(sql, {'id': uid})
            db.session.commit()
        except Exception as error:
            raise DatabaseException('While removing the user') from error


user_repository = UserRepository()
