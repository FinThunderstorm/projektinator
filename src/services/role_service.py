from repositories.role_repository import role_repository, RoleRepository
from utils.exceptions import UnvalidInputException


class RoleService:

    def __init__(self,
                 default_role_repository: RoleRepository = role_repository):
        self._role_repository = default_role_repository

    def get_all(self) -> [tuple]:
        '''get_all is used to list of all roles

        If no roles found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of all roles
        '''
        return self._role_repository.get_all()

    def get_by_id(self, rid: str) -> tuple:
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

        try:
            rid = int(rid)
        except Exception as error:
            raise UnvalidInputException(reason='unvalid formatting of id',
                                        source='role') from error

        return self._role_repository.get_by_id(rid)

    def get_name(self, rid: str) -> str:
        '''get_name is used to get name of role with given id

        Args:
            rid (int): id of role

        Raises:
            DatabaseException: raised if problems while
                interacting with the database
            NotExistingException: raised if role is not
                found with given id

        Returns:
            str: found name
        '''

        try:
            rid = int(rid)
        except Exception as error:
            raise UnvalidInputException(reason='unvalid formatting of id',
                                        source='role') from error

        return self._role_repository.get_name(rid)


role_service = RoleService()
