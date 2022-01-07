from utils.database import db
from utils.exceptions import DatabaseException, NotExistingException


class RoleRepository:
    '''Class for handling Roles in the database
    '''

    def get_all(self) -> [tuple]:
        '''get_all is used to list of all roles

        If no roles found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of all roles
        '''

        sql = '''
            SELECT id, name, description 
            FROM Roles
        '''

        try:
            roles = db.session.execute(sql).fetchall()
        except Exception as error:
            raise DatabaseException('While getting all roles') from error

        return [(role[0], role[1], role[2]) for role in roles]

    def get_by_id(self, rid: int) -> tuple:
        '''get_by_id is used to found role with given id

        Args:
            rid (str): id of the role to be found

        Raises:
            DatabaseException: raised if problems while
                interacting with the database
            NotExistingException: raised if role is not
                found with given id

        Returns:
            tuple: role with given id
        '''

        sql = '''
            SELECT id, name, description 
            FROM Roles
        '''

        try:
            role = db.session.execute(sql, {'id': rid}).fetchone()
        except Exception as error:
            raise DatabaseException('While getting the role') from error

        if not role:
            raise NotExistingException('Role')

        return (role[0], role[1], role[2])

    def get_name(self, rid: int) -> str:
        '''get_name is used to get name of role with given id

        Args:
            rid (int): id of the role

        Raises:
            DatabaseException: raised if problems while
                interacting with the database
            NotExistingException: raised if role is not
                found with given id

        Returns:
            str: found name
        '''

        sql = '''
            SELECT name 
            FROM Roles 
            WHERE id=:id
        '''

        try:
            name = db.session.execute(sql, {'id': rid}).fetchone()
        except Exception as error:
            raise DatabaseException('While getting role´s name') from error

        if not name:
            raise NotExistingException('Role')

        return name[0]


role_repository = RoleRepository()
