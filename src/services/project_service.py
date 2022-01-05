from entities.project import Project

from repositories.user_repository import user_repository, UserRepository
from repositories.project_repository import project_repository, ProjectRepository

from services.feature_service import feature_service, FeatureService

from utils.exceptions import EmptyValueException, UnvalidInputException, NotExistingException
from utils.validators import validate_flags, validate_uuid4
from utils.helpers import fullname


class ProjectService:
    '''Class used for handling projects in the application
    '''

    def __init__(
            self,
            default_project_repository: ProjectRepository = project_repository,
            default_user_repository: UserRepository = user_repository,
            default_feature_service: FeatureService = feature_service):
        '''Initializes ProjectService

        Args:
            default_project_repository (ProjectRepository, optional):
                interaction module with database for projects.
                Defaults to project_repository.
            default_user_repository (UserRepository, optional):
                interaction module with users.
                Defaults to user_repository.
        '''
        self._project_repository = default_project_repository
        self._user_repository = default_user_repository
        self._feature_service = default_feature_service

    def new(self,
            poid: str,
            name: str,
            description: str,
            flags: str = '') -> Project:
        '''new is used to create new projects into the database

        Args:
            poid (str): id of the project's owner
            name (str): name of the project
            description (str): description of the project
            flags (str): flags used to identify projects,
                given in string, example = 'one;two;three;flags;'

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database
            EmptyValueException: raised if any given values is empty
            UnvalidInputException: raised if formatting of given
                input value is incorrect
            NotExistingException: raised if project owner
                with given id is not found

        Returns:
            Project: created project
        '''

        if not poid or not name or not description:
            raise EmptyValueException(
                'One of given values is empty, all values need to have value')

        if not validate_uuid4(poid):
            raise UnvalidInputException('Unvalid formatting',
                                        'not being in correct format of uuid4',
                                        'project owner id')

        poname = self._user_repository.get_fullname(poid)

        if not poname:
            raise NotExistingException('Project Owner')

        if not validate_flags(flags):
            raise UnvalidInputException(
                'Unvalid formatting',
                'not being in "one;two;three;flags;" format', 'flags')

        project_id, created, updated_on = self._project_repository.new(
            poid, name, description, flags)

        created_project = Project(project_id, poid, poname, name, description,
                                  created, updated_on)

        return created_project

    def update(self, pid: str, poid: str, name: str, description: str,
               flags: str) -> Project:
        '''update is used to update project with given values

        Args:
            pid (str): if of the project
            poid (str): id of the project's owner
            name (str): name of the project
            description (str): description of the project
            flags (str): flags used to identify projects,
                given in string, example = 'one;two;three;flags;'

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database
            EmptyValueException: raised if any given values is empty
            UnvalidInputException: raised if formatting of given
                input value is incorrect
            NotExistingException: raised if project owner or project
                with given id is not found

        Returns:
            Project: updated project
        '''
        if not validate_uuid4(pid):
            raise UnvalidInputException('Unvalid formatting',
                                        'not being in correct format of uuid4',
                                        'project id')

        project = self._project_repository.get_by_id(pid)
        if not project:
            raise NotExistingException('Project')

        if not poid or not name or not description or not flags:
            raise EmptyValueException(
                'One of given values is empty, all values need to have value')

        if not validate_uuid4(poid):
            raise UnvalidInputException('Unvalid formatting',
                                        'not being in correct format of uuid4',
                                        'project owner id')

        poname = self._user_repository.get_fullname(poid)

        if not poname:
            raise NotExistingException('Project Owner')

        if not validate_flags(flags):
            raise UnvalidInputException(
                'Unvalid formatting',
                'not being in "one;two;three;flags;" format', 'flags')

        project_id, created, updated_on = self._project_repository.new(
            poid, name, description, flags)

        updated_project = Project(project_id, poid, poname, name, description,
                                  created, updated_on)

        return updated_project

    def get_all(self) -> [Project]:
        '''get_all is used to get list of all projects in the database

        If no projects found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [Project]: list of all projects
        '''

        projects = [
            Project(project[0], project[1], fullname(project[2], project[3]),
                    project[4], project[5], project[6], project[7], project[8],
                    self._feature_service.get_all_by_project_id(project[0]))
            for project in self._project_repository.get_all()
        ]

        return projects

    def get_projects(self) -> [tuple]:
        '''get_projects is used to get all projects for
           selecting projects in the frontend

        If no projects found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of project id and name
        '''
        projects = self._project_repository.get_projects()
        return projects

    def get_all_by_project_owner(self, poid: str) -> [Project]:
        '''get_all_by_project_owner is used get all projects
           associated with given project owner

        If no features found, returns empty list.

        Args:
            poid (str): id of the project's owner

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if user with given
                id not found
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            [tuple]: list of found projects
        '''
        if not validate_uuid4(poid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='Project Owner ID')

        if not self._user_repository.get_by_id(poid):
            raise NotExistingException('Project Owner')

        projects = [
            Project(project[0], project[1], fullname(project[2], project[3]),
                    project[4], project[5], project[6], project[7], project[8],
                    self._feature_service.get_all_by_project_id(project[0])) for
            project in self._project_repository.get_all_by_project_owner(poid)
        ]

        return projects

    def get_by_id(self, pid: str) -> Project:
        '''get_by_id is used to find exact project with given id

        Args:
            pid (str): id of the project

        Raises:
            DatabaseException: raised if problems while
                interacting with the database
            NotExistingException: raised if project is not
                found with given id
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            Project: found project
        '''

        if not validate_uuid4(pid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='Project ID')

        project = self._project_repository.get_by_id(pid)

        return Project(project[0], project[1], fullname(project[2],
                                                        project[3]), project[4],
                       project[5], project[6], project[7], project[8],
                       self._feature_service.get_all_by_project_id(project[0]))

    def get_name(self, pid: str) -> str:
        '''get_name is used to get name of project with given id

        Args:
            pid (str): id of the project

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if project is not
                found with given id
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            str: found name
        '''

        if not validate_uuid4(pid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='Project ID')

        name = self._project_repository.get_name(pid)
        return name

    def remove(self, pid: str) -> None:
        '''remove is used to remove project from database

        Args:
            pid (str): id of the project to be removed

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if project not found with given id
            UnvalidInputException: raised if unvalid
                id is given
        '''

        if not validate_uuid4(pid):
            raise UnvalidInputException('Unvalid formatting',
                                        'not being in correct format of uuid4',
                                        'project id')

        self._project_repository.get_by_id(pid)
        self._project_repository.remove(pid)


project_service = ProjectService()
