from repositories.type_repository import TypeRepository, type_repository
from utils.exceptions import UnvalidInputException
from utils.validators import validate_uuid4


class TypeService:
    '''Class used for handling types in the application'''

    def __init__(self,
                 default_type_repository: TypeRepository = type_repository):
        '''Initializes TypeService

        Args:
            default_type_repository (TypeRepository, optional):
                interaction module with database for types.
                Defaults to type_repository.
        '''
        self._type_repository = default_type_repository

    def get_all(self) -> [tuple]:
        '''get_all is used to list of all types

        If no types found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of all types
        '''
        types = self._type_repository.get_all()
        return types

    def get_by_id(self, tyid: str) -> tuple:
        '''get_by_id is used to found type with given id

        Args:
            rid (str): id of the type to be found

        Raises:
            DatabaseException: raised if problems while
                interacting with the database
            NotExistingException: raised if type is not
                found with given id
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            tuple: type with given id
        '''

        if not validate_uuid4(tyid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='Type ID')

        found_type = self._type_repository.get_by_id(tyid)
        return found_type

    def get_name(self, tyid: str) -> str:
        '''get_name is used to get name of type with given id

        Args:
            rid (int): id of the type

        Raises:
            DatabaseException: raised if problems while
                interacting with the database
            NotExistingException: raised if type is not
                found with given id
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            str: found name
        '''

        if not validate_uuid4(tyid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='Type ID')

        name = self._type_repository.get_name(tyid)
        return name


type_service = TypeService()
