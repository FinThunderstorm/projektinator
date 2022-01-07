from utils.database import db
from utils.exceptions import DatabaseException, NotExistingException


class TypeRepository:
    '''Class for handling Types in the database
    '''

    def get_all(self) -> [tuple]:
        '''get_all is used to list of all types

        If no types found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of all types
        '''

        sql = '''
            SELECT id, name 
            FROM Types
        '''

        try:
            types = db.session.execute(sql).fetchall()
        except Exception as error:
            raise DatabaseException('While getting all types') from error

        return [(type[0], type[1]) for type in types]

    def get_by_id(self, tyid: str) -> tuple:
        '''get_by_id is used to found type with given id

        Args:
            rid (str): id of the type to be found

        Raises:
            DatabaseException: raised if problems while
                interacting with the database
            NotExistingException: raised if type is not
                found with given id

        Returns:
            tuple: type with given id
        '''

        sql = '''
            SELECT id, name 
            FROM Types 
            WHERE id=:id
        '''

        try:
            found_type = db.session.execute(sql, {'id': tyid}).fetchone()
        except Exception as error:
            raise DatabaseException('While getting the type') from error

        if not found_type:
            raise NotExistingException('Type')

        return (found_type[0], found_type[1])

    def get_name(self, tyid: str) -> str:
        '''get_name is used to get name of type with given id

        Args:
            rid (int): id of the type

        Raises:
            DatabaseException: raised if problems while
                interacting with the database
            NotExistingException: raised if type is not
                found with given id

        Returns:
            str: found name
        '''

        sql = '''
            SELECT name 
            FROM Types 
            WHERE id=:id
        '''

        try:
            name = db.session.execute(sql, {'id': tyid}).fetchone()
        except Exception as error:
            raise DatabaseException('While getting type´s name') from error

        if not name:
            raise NotExistingException('Type')

        return name[0]


type_repository = TypeRepository()
