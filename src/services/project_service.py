from datetime import datetime
from entities.project import Project
from repositories.user_repository import user_repository, UserRepository
from repositories.project_repository import project_repository, ProjectRepository
from utils.exceptions import EmptyValueException, UnvalidInputException, NotExistingException
from utils.validators import validate_flags, validate_uuid4


class ProjectService:
    """Class used for handling projects in the application
    """

    def __init__(self, default_project_repository: ProjectRepository = project_repository, default_user_repository: UserRepository = user_repository):
        """Initializes Project Service

        Args:
            default_project_repository (ProjectRepository, optional): interaction module with database for projects. Defaults to project_repository.
            default_user_repository (UserRepository, optional): interaction module with database for users. Defaults to user_repository.
        """
        self._project_repository = default_project_repository
        self._user_repository = default_user_repository

    def new(self, poid: str, name: str, descrption: str, flags: str = "") -> Project:
        """new is used to create new projects into the database

        Args:
            poid (str): id of project owner
            name (str): name of project
            descrption (str): description of project
            flags (str, optional): flags used to filter and label projects. Defaults to "".

        Raises:
            NotExistingException: raised if there is not user with given project owner id
            EmptyValueException: raised if any given values is empty (excluding flags)
            UnvalidInputException: raised if any of id's is not in valid uuid4 format
            DatabaseException: if problem occurs while handling with the database

        Returns:
            Project: newly created project as Project object
        """

        poname = self._user_repository.get_fullname(poid)

        if not poid or not name or not descrption:
            raise EmptyValueException(
                'One of given values is empty, all values need to have value')

        if not validate_uuid4(poid):
            raise UnvalidInputException(
                'Unvalid formatting', "not being in correct format of uuid4", "project owner id")

        if not validate_flags(flags):
            raise UnvalidInputException(
                "Unvalid formatting", "not being in 'one;two;three;flags;' format", "flags")

        created_project = self._project_repository.new(
            poid, poname, name, descrption, flags)
        return created_project

    def update(self, pid: str, poid: str, name: str, descrption: str, flags: str, created: datetime) -> Project:
        """update is used to update project in the database

        Args:
            pid (str): id of project to be updated
            poid (str): id of project owner
            name (str): name of project
            descrption (str): description of project
            flags (str): flags used to filter and label projects.
            created (datetime): creation time of project

        Raises:
            NotExistingException: raised if project not existing
            EmptyValueException: raised if any given values is empty
            UnvalidInputException: raised if any of id's is not in valid uuid4 format
            DatabaseException: if problem occurs while handling with the database

        Returns:
            Project: updated project as Project object
        """
        project = self.get_by_id(pid)
        if not project:
            raise NotExistingException('Project')

        poname = self._user_repository.get_fullname(poid)
        if not poid or not poname or not name or not descrption or not flags or not created:
            raise EmptyValueException(
                'One of given values is empty, all values need to have value')

        if not validate_uuid4(pid):
            raise UnvalidInputException(
                'Unvalid formatting', 'not being in correct format of uuid4', "project id")

        if not validate_uuid4(poid):
            raise UnvalidInputException(
                'Unvalid formatting', "not being in correct format of uuid4", "project owner id")

        if not validate_flags(flags):
            raise UnvalidInputException(
                "Unvalid formatting", "not being in 'one;two;three;flags;' format", "flags")

        updated_project = self._project_repository.update(
            pid, poid, poname, name, descrption, flags, created)

        return updated_project

    def get_all(self) -> [Project]:
        """get_all is used to get list of all projects in the database

        Raises:
            DatabaseException: raised if problems occur while interacting with the database

        Returns:
            [Project]: list of all projects as project objects
        """
        projects = self._project_repository.get_all()
        return projects

    def get_all_by_project_owner(self, poid: str) -> [Project]:
        """get_all_by_project_owner is used to get list of all projects associated with given project owner in the database

        Raises:
            DatabaseException: raised if problems occur while interacting with the database
            NotExistingException: raised if there is none projects associated with given project owner or not given project owner found
        Returns:
            [Project]: list of all projects as project objects
        """
        if not self._user_repository.get_by_id(poid):
            raise NotExistingException('Project owner')
        projects = self._project_repository.get_all_by_project_owner(poid)
        return projects

    def get_by_id(self, pid: str) -> Project:
        """get_by_id is used to find exact project with given id from the database

        Args:
            pid (str): id of project to be found

        Raises:
            DatabaseException: raised if problems occur while interacting with the database
            NotExistingException: raised if there is none projects with given id

        Returns:
            Project: project with given id
        """
        project = self._project_repository.get_by_id(pid)
        return project

    def remove(self, pid: str) -> None:
        """remove is used to remove project's from database

        Args:
            pid (str): id of project to be removed

        Raises:
            NotExistingException: raised if project not found with given id
            DatabaseException: raised if problems while interacting with database
        """
        if not self.get_by_id(pid):
            raise NotExistingException('Project')
        self._project_repository.remove(pid)


project_service = ProjectService()
