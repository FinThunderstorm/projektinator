from repositories.status_repository import StatusRepository, status_repository
from utils.exceptions import UnvalidInputException
from utils.validators import validate_uuid4


class StatusService:

    def __init__(
            self,
            default_status_repository: StatusRepository = status_repository):
        '''Initializes StatusServce

        Args:
            default_status_repository (StatusRepository, optional):
                interaction module with database for statuses.
                Defaults to status_repository.
        '''
        self._status_repository = default_status_repository

    def get_all(self):
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

        statuses = self._status_repository.get_all()
        return statuses

    def get_by_id(self, sid: str):
        '''get_by_id is used to found status with given id

        Args:
            rid (str): id of the status to be found

        Raises:
            DatabaseException: raised if problems while
                interacting with the database
            NotExistingException: raised if status is not
                found with given id
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            tuple: status with given id
        '''

        if not validate_uuid4(sid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='Status ID')

        status = self._status_repository.get_by_id(sid)
        return status

    def get_name(self, sid: str):
        '''get_name is used to get name of status with given id

        Args:
            rid (int): id of the status

        Raises:
            DatabaseException: raised if problems while
                interacting with the database
            NotExistingException: raised if status is not
                found with given id
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            str: found name
        '''

        if not validate_uuid4(sid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='Status ID')

        name = self._status_repository.get_name(sid)
        return name


status_service = StatusService()
