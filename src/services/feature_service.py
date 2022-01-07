from entities.feature import Feature

from repositories.project_repository import project_repository, ProjectRepository
from repositories.feature_repository import feature_repository, FeatureRepository
from repositories.type_repository import type_repository, TypeRepository
from repositories.status_repository import status_repository, StatusRepository
from repositories.user_repository import user_repository, UserRepository

from services.task_service import task_service, TaskService
from services.comment_service import comment_service, CommentService

from utils.exceptions import EmptyValueException, UnvalidInputException, NotExistingException
from utils.validators import validate_flags, validate_uuid4
from utils.helpers import fullname


class FeatureService:
    '''Class used for handling features in the application'''

    def __init__(
            self,
            default_project_repository: ProjectRepository = project_repository,
            default_feature_repository: FeatureRepository = feature_repository,
            default_type_repository: TypeRepository = type_repository,
            default_status_repository: StatusRepository = status_repository,
            default_user_repository: UserRepository = user_repository,
            default_task_service: TaskService = task_service,
            default_comment_service: CommentService = comment_service):
        '''Initializes FeatureService

        Args:
            default_project_repository (ProjectRepository, optional):
                interaction module with database for projects.
                Defaults to project_repository.
            default_feature_repository (FeatureRepository, optional):
                interaction module with database for features.
                Defaults to feature_repository.
            default_type_repository (TypeRepository, optional):
                interaction module with database for types.
                Defaults to feature_repository.
            default_status_repository (StatusRepository, optional):
                interaction module with database for statuses.
                Defaults to status_repository.
            default_user_repository (UserRepository, optional):
                interaction module with database for users.
                Defaults to user_repository.
            default_task_service (TaskService, optional):
                interaction module with tasks.
                Defaults to task_service.
            default_comment_service (CommentService, optional):
                interaction module with comments.
                Defaults to comment_service.
        '''

        self._project_repository = default_project_repository
        self._feature_repository = default_feature_repository
        self._type_repository = default_type_repository
        self._status_repository = default_status_repository
        self._user_repository = default_user_repository
        self._task_service = default_task_service
        self._comment_service = default_comment_service

    def new(
        self,
        pid: str,
        foid: str,
        name: str,
        description: str,
        status: str,
        ftype: str,
        priority: str,
        flags: str = '',
    ) -> Feature:
        '''new is used to create new features

        Args:
            pid (str): id of associated project
            foid (str): id of associated feature owner
            name (str): name of feature
            description (str): description of feature
            status (str): status of feature, for example
                'in progress', 'waiting', 'ready', 'postponed'
            ftype (str): type of feature, for example 'new feature',
                'bug fixes', 'refactoring'
            priority (str): priority of feature, in three stages:
                low, medium and high (1 = low, 3 = high)
            flags (str): flags used to identify features,
                given in string, example = 'one;two;flags;'

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database
            EmptyValueException: raised if any given values is empty
            UnvalidInputException: raised if formatting of given
                input value is incorrect
            NotExistingException: raised if feature owner or project
                with given id is not found

        Returns:
            Feature: created feature
        '''

        if len(name) > 100 or len(description) > 1000 or len(flags) > 1000:
            raise UnvalidInputException('Input values too long')

        if (not pid or not foid or not name or not description or not status
                or not ftype or not priority):
            raise EmptyValueException(
                'One of given values is empty, all values need to have value')

        if not validate_uuid4(pid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='project id')
        if not validate_uuid4(foid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='feature owner id')
        if not validate_uuid4(ftype):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='feature type id')
        if not validate_uuid4(status):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='status id')

        if not validate_flags(flags):
            raise UnvalidInputException(
                'Unvalid formatting',
                'not being in 'one;two;three;flags;' format', 'flags')

        try:
            priority = int(priority)
        except Exception as error:
            raise UnvalidInputException(
                reason='can not be converted into integer',
                source='priority') from error

        if not 1 <= priority <= 3:
            raise UnvalidInputException(reason='priority is not in scale 1-3',
                                        source='priority')

        pname = self._project_repository.get_name(pid)
        foname = self._user_repository.get_fullname(foid)
        sname = self._status_repository.get_name(status)
        ftname = self._type_repository.get_name(ftype)

        if not pname:
            raise NotExistingException('Project')
        if not foname:
            raise NotExistingException('Feature Owner')
        if not sname:
            raise NotExistingException('Status')
        if not ftname:
            raise NotExistingException('Feature Type')

        feature_id, created, updated_on = self._feature_repository.new(
            pid, foid, name, description, flags, status, ftype, priority)

        created_feature = Feature(feature_id, pid, pname, foid, foname, name,
                                  description, status, sname, ftype, ftname,
                                  priority, created, updated_on)
        return created_feature

    def get_all(self) -> [Feature]:
        '''get_all is used to list of all features in the database

        If no features found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [Feature]: list of all features
        '''

        features = [
            Feature(feature[0], feature[1], feature[2], feature[3],
                    fullname(feature[4], feature[5]), feature[6], feature[7],
                    feature[8], feature[9], feature[10], feature[11],
                    feature[12], feature[13], feature[14], feature[15],
                    self._task_service.get_all_by_feature_id(feature[0]),
                    self._comment_service.get_all_by_feature_id(feature[0]))
            for feature in self._feature_repository.get_all()
        ]

        return features

    def get_features(self) -> [tuple]:
        '''get_features is used to get all features for
           selecting features in the frontend

        If no features found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of feature id and name
        '''

        features = self._feature_repository.get_features()
        return features

    def get_all_by_project_id(self, pid: str) -> [Feature]:
        '''get_all_by_project_id is used to get all features
           associated with given project

        If no features found, returns empty list.

        Args:
            pid (str): id of the project in which features are associated

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if project with given
                id not found
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            [Feature]: list of found features
        '''

        if not validate_uuid4(pid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='project id')

        if not self._project_repository.get_by_id(pid):
            raise NotExistingException('Project')

        features = [
            Feature(feature[0], feature[1], feature[2], feature[3],
                    fullname(feature[4], feature[5]), feature[6], feature[7],
                    feature[8], feature[9], feature[10], feature[11],
                    feature[12], feature[13], feature[14], feature[15],
                    self._task_service.get_all_by_feature_id(feature[0]),
                    self._comment_service.get_all_by_feature_id(feature[0]))
            for feature in self._feature_repository.get_all_by_project_id(pid)
        ]
        return features

    def get_all_by_feature_owner(self, foid: str) -> [Feature]:
        '''get_all_by_feature_owner is used get all features
           associated with given feature owner

        If no features found, returns empty list.

        Args:
            foid (str): id of the feature owner

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if user with given
                id not found
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            [Feature]: list of found features
        '''

        if not validate_uuid4(foid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='feature owner´s id')

        if not self._user_repository.get_by_id(foid):
            raise NotExistingException('Feature owner')

        features = [
            Feature(feature[0], feature[1], feature[2], feature[3],
                    fullname(feature[4], feature[5]), feature[6], feature[7],
                    feature[8], feature[9], feature[10], feature[11],
                    feature[12], feature[13], feature[14], feature[15],
                    self._task_service.get_all_by_feature_id(feature[0]),
                    self._comment_service.get_all_by_feature_id(feature[0])) for
            feature in self._feature_repository.get_all_by_feature_owner(foid)
        ]
        return features

    def get_by_id(self, fid: str) -> Feature:
        '''get_by_id is used to found feature with given id

        Args:
            fid (str): id of feature to be found

        Raises:
            DatabaseException: raised if problems while
                interacting with the database
            NotExistingException: raised if feature is not
                found with given id
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            Feature: feature with given id
        '''

        if not validate_uuid4(fid):
            raise UnvalidInputException('feature´s id')

        feature = self._feature_repository.get_by_id(fid)

        return Feature(feature[0], feature[1], feature[2], feature[3],
                       fullname(feature[4], feature[5]), feature[6], feature[7],
                       feature[8], feature[9], feature[10], feature[11],
                       feature[12], feature[13], feature[14], feature[15],
                       self._task_service.get_all_by_feature_id(feature[0]),
                       self._comment_service.get_all_by_feature_id(feature[0]))

    def get_name(self, fid: str) -> str:
        '''get_name is used to get name of feature with given id

        Args:
            fid (str): id of feature

        Raises:
            DatabaseException: raised if problems while
                interacting with the database
            NotExistingException: raised if feature is not
                found with given id
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            str: found name
        '''

        if not validate_uuid4(fid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='feature id')

        feature_name = self._feature_repository.get_name(fid)
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
    ) -> Feature:
        '''update is used to update feature with given values

        Args:
            fid (str): id of feature to be updated
            pid (str): id of associated project
            foid (str): id of associated feature owner
            name (str): name of feature
            description (str): description of feature
            flags (str): flags used to identify features,
                given in string, example = 'one;two;flags;'
            status (str): status of feature, for example
                'in progress', 'waiting', 'ready', 'postponed'
            ftype (str): type of feature, for example
                'new feature', 'bug fixes', 'refactoring'
            priority (str): priority of feature, in three stages:
                low, medium and high (1 = low, 3 = high)

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database
            EmptyValueException: raised if any given values is empty
            UnvalidInputException: raised if formatting of given
                input value is incorrect
            NotExistingException: raised if feature, feature owner or project
                with given id is not found


        Returns:
            Project: updated feature as Feature object
        '''

        if len(name) > 100 or len(description) > 1000 or len(flags) > 1000:
            raise UnvalidInputException('Input values too long')

        if (not fid or not pid or not foid or not name or not description
                or not status or not ftype or not priority):
            raise EmptyValueException(
                'One of given values is empty, all values need to have value')

        if not validate_uuid4(fid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='feature id')

        feature = self._feature_repository.get_by_id(fid)
        if not feature:
            raise NotExistingException('Feature')

        if not validate_uuid4(pid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='project id')
        if not validate_uuid4(foid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='feature owner id')
        if not validate_uuid4(ftype):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='feature type id')
        if not validate_uuid4(status):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='status id')

        if not validate_flags(flags):
            raise UnvalidInputException(
                'Unvalid formatting',
                'not being in 'one;two;three;flags;' format', 'flags')

        try:
            priority = int(priority)
        except Exception as error:
            raise UnvalidInputException(
                reason='can not be converted into integer',
                source='priority') from error

        if not 1 <= priority <= 3:
            raise UnvalidInputException(reason='priority is not in scale 1-3',
                                        source='priority')

        pname = self._project_repository.get_name(pid)
        foname = self._user_repository.get_fullname(foid)
        sname = self._status_repository.get_name(status)
        ftname = self._type_repository.get_name(ftype)

        if not pname:
            raise NotExistingException('Project')
        if not foname:
            raise NotExistingException('Feature owner')
        if not sname:
            raise NotExistingException('Status')
        if not ftname:
            raise NotExistingException('Feature Type')

        feature_id, created, updated_on = self._feature_repository.update(
            fid, pid, foid, name, description, flags, status, ftype, priority)
        return Feature(feature_id, pid, pname, foid, foname, name, description,
                       status, sname, ftype, ftname, priority, created,
                       updated_on)

    def remove(self, fid: str):
        '''remove is used to remove feature

        Args:
            fid (str): id of feature to be removed

        Raises:
            DatabaseException: raised if problems occurs
                while interacting with database.
            NotExistingException: raised if feature not found with given id
            UnvalidInputException: raised if unvalid
                id is given
        '''

        if not validate_uuid4(fid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='feature id')

        self._feature_repository.get_by_id(fid)
        self._feature_repository.remove(fid)


feature_service = FeatureService()
