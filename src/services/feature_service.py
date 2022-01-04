from datetime import datetime
from entities.feature import Feature
from entities.project import Project
from repositories.user_repository import user_repository, UserRepository
from repositories.project_repository import project_repository, ProjectRepository
from repositories.feature_repository import feature_repository, FeatureRepository
from repositories.type_repository import TypeRepository, type_repository
from repositories.status_repository import StatusRepository, status_repository
from utils.exceptions import EmptyValueException, UnvalidInputException, NotExistingException
from utils.validators import validate_flags, validate_uuid4


class FeatureService:
    """Class used for handling projects in the application"""

    def __init__(
            self,
            default_feature_repository: FeatureRepository = feature_repository,
            default_project_repository: ProjectRepository = project_repository,
            default_user_repository: UserRepository = user_repository,
            default_status_repository: StatusRepository = status_repository,
            default_type_repository: TypeRepository = type_repository):
        """Initializes FeatureService

        Args:
            default_feature_repository (FeatureRepository, optional): interaction module with database for features. Defaults to feature_repository.
            default_project_repository (ProjectRepository, optional): interaction module with database for projects. Defaults to project_repoistory.
            default_user_repository (UserRepository, optional): interaction module with database for users. Defaults to user_repository.
        """
        self._feature_repository = default_feature_repository
        self._project_repository = default_project_repository
        self._user_repository = default_user_repository
        self._status_repository = default_status_repository
        self._type_repository = default_type_repository

    def new(
        self,
        pid: str,
        foid: str,
        name: str,
        description: str,
        status: str,
        ftype: str,
        priority: str,
        flags: str = "",
    ) -> Feature:
        """new is used to create new features

        Args:
            pid (str): id of associated project
            foid (str): id of associated feature owner
            name (str): name of feature
            description (str): description of feature
            flags (str): flags used to identify features, given in string, example = "one;two;flags;"
            status (str): status of feature, for example "in progress", "waiting", "ready", "postponed"
            ftype (str): type of feature, for example "new feature", "bug fixes"
            priority (int): priority of feature, in three stages: low, severe and high (1 = low, 3 = high)

        Raises:
            DatabaseException: raised if problems occurs while saving into the database
            EmptyValueException: raised if any given values is empty
            UnvalidInputException: raised if formatting of given input value is incorrect
            NotExistingException: raised if feature owner or project with given id is not found

        Returns:
            Feature: created feature as Feature object
        """
        if (not pid or not foid or not name or not description or not status
                or not ftype or not priority):
            raise EmptyValueException(
                "One of given values is empty, all values need to have value")

        if not validate_uuid4(pid):
            raise UnvalidInputException(reason="unvalid formatting of uuid4",
                                        source="project id")
        if not validate_uuid4(foid):
            raise UnvalidInputException(reason="unvalid formatting of uuid4",
                                        source="feature owner id")
        if not validate_flags(flags):
            raise UnvalidInputException(
                "Unvalid formatting",
                "not being in 'one;two;three;flags;' format", "flags")

        try:
            priority = int(priority)
        except Exception as error:
            raise UnvalidInputException(
                reason="can not be converted into integer",
                source="priority") from error

        if priority < 0 or priority > 3:
            raise UnvalidInputException(reson="priority is not in scale 1-3",
                                        source="priority")

        pname = self._project_repository.get_name(pid)
        foname = self._user_repository.get_fullname(foid)
        sname = self._status_repository.get_name(status)
        ftname = self._type_repository.get_name(ftype)

        if not pname:
            raise NotExistingException("Project")
        if not foname:
            raise NotExistingException("Feature owner")

        created_feature = self._feature_repository.new(pid, pname, foid, foname,
                                                       name, description, flags,
                                                       status, sname, ftype,
                                                       ftname, priority)
        return created_feature

    def get_all(self) -> [Feature]:
        """get_all is used to list of all features

        Raises:
            DatabaseException: raised if problems occur while interacting with the database
            NotExistingException: raised if any features is not found

        Returns:
            [Feature]: list of all features as Feature object
        """

        features = self._feature_repository.get_all()
        if not features:
            raise NotExistingException("Features", "not found.")
        return features

    def get_features(self) -> list[tuple]:
        """get_features is used to get all features for selecting features in the frontend

        Raises:
            DatabaseException: raised if problems occur while interacting with the database

        Returns:
            list[tuple]: list of feature id and name
        """

        features = self._feature_repository.get_features()
        return features

    def get_all_by_project_id(self, pid: str) -> [Feature]:
        """get_all_by_project_id is used to get all features associated with given project

        Args:
            pid (str): id of project in which features must be associated

        Raises:
            DatabaseException: raised if problem occurs while interacting with the database
            NotExistingException: raised if any features is not found, or project with given id not found

        Returns:
            [Feature]: list of found features
        """
        if not self._project_repository.get_by_id(pid):
            raise NotExistingException("Project")

        features = self._feature_repository.get_all_by_project_id()
        if not features:
            raise NotExistingException("Features")
        return features

    def get_all_by_feature_owner(self, foid: str) -> [Feature]:
        """get_all_by_project_id is used to get all features associated with given project

        Args:
            foid (str): id of user in which features must be associated

        Raises:
            DatabaseException: raised if problem occurs while interacting with the database
            NotExistingException: raised if any features is not found, or user with given id not found

        Returns:
            [Feature]: list of found features
        """
        if not self._user_repository.get_by_id(foid):
            raise NotExistingException("Feature owner")

        features = self._feature_repository.get_all_by_feature_owner(foid)
        if not features:
            raise NotExistingException("Features")
        return features

    def get_by_id(self, fid: str) -> Feature:
        """get_by_id is used to found feature with given id

        Args:
            fid (str): id of feature to be found

        Raises:
            DatabaseException: raised if problems while interacting with the database
            NotExistingException: raised if feature not found with given id

        Returns:
            Feature: found feature
        """
        feature = self._feature_repository.get_by_id(fid)
        if not feature:
            raise NotExistingException("Feature")
        return feature

    def get_name(self, fid: str) -> str:
        """get_name is used to get name of feature with given id

        Args:
            fid (str): id of feature

        Raises:
            DatabaseException: raised if problems while interacting with the database
            NotExistingException: raised if feature not found with given id

        Returns:
            Feature: found feature
        """
        feature_name = self._feature_repository.get_name(fid)
        if not feature_name:
            raise NotExistingException("Feature")
        return feature_name

    def update(
        self,
        fid: str,
        pid: str,
        foid: str,
        name: str,
        description: str,
        flags: str,
        status: str,
        ftype: str,
        priority: str,
    ) -> Project:
        """update is used to update feature with given values

        Args:
            fid (str): id of feature to be updated
            pid (str): id of associated project
            foid (str): id of associated feature owner
            name (str): name of feature
            description (str): description of feature
            flags (str): flags used to identify features, given in string, example = "one;two;flags;"
            status (str): status of feature, for example "in progress", "waiting", "ready", "postponed"
            ftype (str): type of feature, for example "new feature", "bug fixes"
            priority (str): priority of feature, in three stages: low, severe and high (1 = low, 3 = high)

        Raises:
            EmptyValueException: raised if any given values is empty
            UnvalidInputException: raised if formatting of given input value is incorrect
            NotExistingException: raised if feature owner or project with given id is not found
            DatabaseException: raised if problems occurs while saving into the database.


        Returns:
            Project: updated feature as Feature object
        """
        if (not fid or not pid or not foid or not name or not description
                or not status or not ftype or not priority):
            raise EmptyValueException(
                "One of given values is empty, all values need to have value")

        feature = self._feature_repository.get_by_id(fid)
        if not feature:
            raise NotExistingException("Feature")

        if not validate_uuid4(pid):
            raise UnvalidInputException(reason="unvalid formatting of uuid4",
                                        source="project id")
        if not validate_uuid4(foid):
            raise UnvalidInputException(reason="unvalid formatting of uuid4",
                                        source="feature owner id")
        if not validate_flags(flags):
            raise UnvalidInputException(
                "Unvalid formatting",
                "not being in 'one;two;three;flags;' format", "flags")

        try:
            priority = int(priority)
        except Exception as error:
            raise UnvalidInputException(
                reason="can not be converted into integer",
                source="priority") from error

        if priority < 0 or priority > 3:
            raise UnvalidInputException(reson="priority is not in scale 1-3",
                                        source="priority")

        pname = self._project_repository.get_name(pid)
        foname = self._user_repository.get_fullname(foid)
        sname = self._status_repository.get_name(status)
        ftname = self._type_repository.get_name(ftype)

        if not pname:
            raise NotExistingException("Project")
        if not foname:
            raise NotExistingException("Feature owner")

        updated_feature = self._feature_repository.update(
            fid, pid, pname, foid, foname, name, description, flags, status,
            sname, ftype, ftname, priority)
        return updated_feature

    def remove(self, fid: str) -> None:
        """remove is used to remove feature

        Args:
            fid (str): id of feature which is removed

        Raises:
            DatabaseException: raised if problems occurs while interacting with database.
            NotExistingException: raised if feature not found with given id
        """
        if not self._feature_repository.get_by_id(fid):
            raise NotExistingException("Feature")
        self._feature_repository.remove(fid)


feature_service = FeatureService()
