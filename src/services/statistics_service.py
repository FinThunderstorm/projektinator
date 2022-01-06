from repositories.statistics_repository import statistics_repository, StatisticsRepository
from repositories.feature_repository import feature_repository, FeatureRepository
from repositories.task_repository import task_repository, TaskRepository
from repositories.user_repository import user_repository, UserRepository

from utils.exceptions import UnvalidInputException
from utils.validators import validate_uuid4


class StatisticsService:
    '''Class used for handling statistics in the application'''

    def __init__(
        self,
        default_statistics_repository:
        StatisticsRepository = statistics_repository,
        default_feature_repository: FeatureRepository = feature_repository,
        default_task_repository: TaskRepository = task_repository,
        default_user_repository: UserRepository = user_repository,
    ):
        '''Initializes StatsticsService

        Args:
            default_statistics_repository (StatisticsRepository, optional):
                interaction module with database for statistics.
                Defaults to statistics_repository.
            default_feature_repository (FeatureRepository, optional):
                interaction module with database for statistics.
                Defaults to feature_repository.
            default_task_repository (TaskRepository, optional):
                interaction module with database for statistics.
                Defaults to task_repository.
            default_user_repository (UserRepository, optional):
                interaction module with database for statistics.
                Defaults to user_repository.
        '''

        self._statistics_repository = default_statistics_repository
        self._feature_repository = default_feature_repository
        self._task_repository = default_task_repository
        self._user_repository = default_user_repository

    def db_health(self):
        '''db_health tells if db can be reached

        Raises:
            OperationalError: raised if database is not reachable
        '''

        self._statistics_repository.db_health()

    def get_time_spent_by_task(self, tid: str) -> float:
        '''get_time_spent_by_task is used to get time spent of task

        Args:
            tid (str): id of the task

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if there is none time spent found
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            float: counted time spent
        '''

        if not validate_uuid4(tid):
            raise UnvalidInputException("task's id")

        self._task_repository.get_by_id(tid)

        time_spent = self._statistics_repository.get_time_spent_by_task(tid)

        return time_spent

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

        if not validate_uuid4(fid):
            raise UnvalidInputException("feature's id")

        self._feature_repository.get_by_id(fid)

        time_spent = self._statistics_repository.get_time_spent_by_feature(fid)

        return time_spent

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

        if not validate_uuid4(uid):
            raise UnvalidInputException("users's id")

        self._user_repository.get_by_id(uid)

        time_spent = self._statistics_repository.get_time_spent_by_user(uid)

        return time_spent


statistics_service = StatisticsService()
