from utils.database import db
from utils.exceptions import DatabaseException, NotExistingException


class StatusRepository:
    '''Class for handling Statuses in the database
    '''

    def get_all(self) -> [tuple]:
        '''get_all is used to list of all statuses

        If no statuses found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of all statuses
        '''

        sql = '''
            SELECT id, name 
            FROM Statuses
        '''

        try:
            statuses = db.session.execute(sql).fetchall()
        except Exception as error:
            raise DatabaseException('While getting all statuses') from error

        return [(status[0], status[1]) for status in statuses]

    def get_by_id(self, sid: str) -> tuple:
        '''get_by_id is used to found status with given id

        Args:
            rid (str): id of the status to be found

        Raises:
            DatabaseException: raised if problems while
                interacting with the database
            NotExistingException: raised if status is not
                found with given id

        Returns:
            tuple: status with given id
        '''

        sql = '''
            SELECT id, name 
            FROM Statuses 
            WHERE id=:id
        '''

        try:
            status = db.session.execute(sql, {'id': sid}).fetchone()
        except Exception as error:
            raise DatabaseException('While getting the status') from error

        if not status:
            raise NotExistingException('Status')

        return (status[0], status[1])

    def get_name(self, sid: str) -> str:
        '''get_name is used to get name of status with given id

        Args:
            rid (int): id of the status

        Raises:
            DatabaseException: raised if problems while
                interacting with the database
            NotExistingException: raised if status is not
                found with given id

        Returns:
            str: found name
        '''

        sql = '''
            SELECT name 
            FROM Statuses 
            WHERE id=:id
        '''

        try:
            name = db.session.execute(sql, {'id': sid}).fetchone()
        except Exception as error:
            raise DatabaseException("While getting status' name") from error

        if not name:
            raise NotExistingException('Status')

        return name[0]


status_repository = StatusRepository()
