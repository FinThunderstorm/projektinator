from utils.database import db
from utils.exceptions import DatabaseException, NotExistingException


class StatisticsRepository:
    '''Class for handling Statistics in the database
    '''

    def db_health(self):
        '''db_health tells if db can be reached

        Raises:
            OperationalError: raised if database is not reachable
        '''

        sql = '''
            SELECT 1
        '''

        db.session.execute(sql)

    def get_time_spent_by_task(self, tid: str) -> float:
        '''get_time_spent_by_task is used to get time spent of task

        Args:
            tid (str): id of the task

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if there is none time spent found

        Returns:
            float: counted time spent
        '''

        sql = '''
            SELECT SUM(time_spent)
            FROM Comments
            WHERE task_id=:id
        '''

        try:
            time_spent = db.session.execute(sql, {'id': tid}).fetchone()
        except Exception as error:
            raise DatabaseException(
                'While getting the statistics for task') from error

        if not time_spent:
            raise NotExistingException('Time spent for task')

        return time_spent[0]

    def get_time_spent_by_feature(self, fid: str) -> float:
        '''get_time_spent_by_feature is used to get time spent of feature

        Args:
            fid (str): id of the feature

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if there is none time spent found

        Returns:
            float: counted time spent
        '''

        sql = '''
            SELECT SUM(time_spent)
            FROM Comments
            WHERE feature_id=:id
        '''

        try:
            time_spent = db.session.execute(sql, {'id': fid}).fetchone()
        except Exception as error:
            raise DatabaseException(
                'While getting the statistics for task') from error

        if not time_spent:
            raise NotExistingException('Time spent for task')

        return time_spent[0]

    def get_time_spent_by_user(self, uid: str) -> float:
        '''get_time_spent_by_user is used to get time spent of user

        Args:
            uid (str): id of the user

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if there is none time spent found

        Returns:
            float: counted time spent
        '''

        sql = '''
            SELECT SUM(time_spent)
            FROM Comments
            WHERE assignee=:id
        '''

        try:
            time_spent = db.session.execute(sql, {'id': uid}).fetchone()
        except Exception as error:
            raise DatabaseException(
                'While getting the statistics for user') from error

        if not time_spent:
            raise NotExistingException('Time spent for user')

        return time_spent[0]


statistics_repository = StatisticsRepository()
