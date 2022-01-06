from entities.task import Task

from repositories.task_repository import task_repository, TaskRepository
from repositories.feature_repository import feature_repository, FeatureRepository
from repositories.user_repository import user_repository, UserRepository

from services.type_service import type_service, TypeService
from services.status_service import status_service, StatusService
from services.comment_service import comment_service, CommentService

from utils.exceptions import EmptyValueException, NotExistingException, UnvalidInputException
from utils.validators import validate_flags, validate_uuid4
from utils.helpers import fullname


class TaskService:
    '''Class used for handling users in the application
    '''

    def __init__(
        self,
        default_task_repository: TaskRepository = task_repository,
        default_feature_repository: FeatureRepository = feature_repository,
        default_user_repository: UserRepository = user_repository,
        default_status_service: StatusService = status_service,
        default_type_service: TypeService = type_service,
        default_comment_service: CommentService = comment_service,
    ):
        '''Initializes FeatureService

        Args:
            default_task_repository (TaskRepository, optional):
                interaction module with database for tasks.
                Defaults to task_repository.
            default_feature_repository (FeatureRepository, optional):
                interaction module with database for features.
                Defaults to feature_repository.
            default_user_repository (UserRepository, optional):
                interaction module with database for users.
                Defaults to user_repostory.
            default_status_service (StatusService, optional):
                interaction module with statuses.
                Defaults to status_service.
            default_type_service (TypeService, optional):
                interaction module with types.
                Defaults to type_service.
            default_comment_service (CommentService, optional):
                interaction module with comments.
                Defaults to comment_service.

        '''
        self._task_repository = default_task_repository
        self._feature_repository = default_feature_repository
        self._user_repository = default_user_repository
        self._status_service = default_status_service
        self._type_service = default_type_service
        self._comment_service = default_comment_service

    def new(self,
            fid: str,
            aid: str,
            name: str,
            description: str,
            status: str,
            ttype: str,
            priority: int,
            flags: str = '') -> Task:
        '''new is used to create new tasks into the database

        Args:
            fid (str): id of associated feature
            aid (str): id of associated assignee
            name (str): name of task
            description (str): description of task
            status (str): status of task, for example
                'in progress', 'waiting', 'ready', 'postponed'
            ttype (str): type of task, for example
                'new feature', 'bug fixes'
            priority (int): priority of task, in three stages:
                low, medium and high (1 = low, 3 = high)
            flags (str): flags used to identify tasks,
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
            Task: created task
        '''

        if (not fid or not aid or not name or not description or not status
                or not ttype or not priority):
            raise EmptyValueException(
                'One of given values is empty, all values need to have value')

        if not validate_uuid4(fid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='feature id')
        if not validate_uuid4(aid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='assignee')
        if not validate_uuid4(ttype):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='task type id')
        if not validate_uuid4(status):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='status id')

        if not validate_flags(flags):
            raise UnvalidInputException(
                'Unvalid formatting',
                'not being in "one;two;three;flags;" format', 'flags')

        try:
            priority = int(priority)
        except Exception as error:
            raise UnvalidInputException(
                reason='can not be converted into integer',
                source='priority') from error

        if not 1 <= priority <= 3:
            raise UnvalidInputException(reson='priority is not in scale 1-3',
                                        source='priority')

        fname = self._feature_repository.get_name(fid)
        aname = self._user_repository.get_fullname(aid)
        sname = self._status_service.get_name(status)
        ttname = self._type_service.get_name(ttype)

        if not fname:
            raise NotExistingException('Feature')
        if not aname:
            raise NotExistingException('Assignee')
        if not sname:
            raise NotExistingException('Status')
        if not ttname:
            raise NotExistingException('Type')

        task_id, created, updated_on = self._task_repository.new(
            fid, aid, name, description, status, ttype, priority, flags)

        created_task = Task(task_id, fid, fname, aid, aname, name, description,
                            status, sname, ttype, ttname, priority, created,
                            updated_on, flags)
        return created_task

    def get_all(self) -> [Task]:
        '''get_all is used to get all tasks from the database

        If no tasks found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [Task]: list of all found tasks
        '''

        tasks = [
            Task(task[0], task[1], task[2], task[3], fullname(task[4], task[5]),
                 task[6], task[7], task[8], task[9], task[10], task[11],
                 task[12], task[13], task[14], task[15],
                 self._comment_service.get_all_by_task_id(task[0]))
            for task in self._task_repository.get_all()
        ]

        return tasks

    def get_all_by_feature_id(self, fid: str) -> [Task]:
        '''get_all_by_feature_id is used to get all tasks
           associated with given task

        If no tasks found, returns empty list.

        Args:
            fid (str): id of the feature in which tasks are associated

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if feature with given
                id not found
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            [Task]: list of all found tasks
        '''

        if not validate_uuid4(fid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='Feature ID')

        if not self._feature_repository.get_by_id(fid):
            raise NotExistingException('Feature')

        tasks = [
            Task(task[0], task[1], task[2], task[3], fullname(task[4], task[5]),
                 task[6], task[7], task[8], task[9], task[10], task[11],
                 task[12], task[13], task[14], task[15],
                 self._comment_service.get_all_by_task_id(task[0]))
            for task in self._task_repository.get_all_by_feature_id(fid)
        ]

        return tasks

    def get_all_by_assignee(self, aid: str) -> [Task]:
        '''get_all_by_feature_id is used to get all tasks
           associated with given task

        If no tasks found, returns empty list.

        Args:
            fid (str): id of the feature in which tasks are associated

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if user with given
                id not found
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            [Task]: list of all found tasks
        '''

        if not validate_uuid4(aid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source="assignee's id")

        if not self._user_repository.get_by_id(aid):
            raise NotExistingException('Assignee')

        tasks = [
            Task(task[0], task[1], task[2], task[3], fullname(task[4], task[5]),
                 task[6], task[7], task[8], task[9], task[10], task[11],
                 task[12], task[13], task[14], task[15],
                 self._comment_service.get_all_by_task_id(task[0]))
            for task in self._task_repository.get_all_by_assignee(aid)
        ]

        return tasks

    def get_by_id(self, tid: str) -> Task:
        '''get_by_id is used to found task with given id

        Args:
            tid (str): id of the task

        Raises:
            DatabaseException: raised if problems while
                interacting with the database
            NotExistingException: raised if task is not
                found with given id
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            Task: task with given id
        '''
        if not validate_uuid4(tid):
            raise UnvalidInputException("tasks's id")

        task = self._task_repository.get_by_id(tid)

        return Task(task[0], task[1], task[2], task[3],
                    fullname(task[4],
                             task[5]), task[6], task[7], task[8], task[9],
                    task[10], task[11], task[12], task[13], task[14], task[15],
                    self._comment_service.get_all_by_task_id(task[0]))

    def get_name(self, tid: str) -> str:
        '''get_name is used to get name of specific task

        Args:
            tid (str): if of the task

        Raises:
            DatabaseException: raised if problems while
                interacting with the database
            NotExistingException: raised if task is not
                found with given id
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            str: found name
        '''

        if not validate_uuid4(tid):
            raise UnvalidInputException("tasks's id")

        name = self._task_repository.get_name(tid)

        return name

    def update(self, tid: str, fid: str, aid: str, name: str, description: str,
               status: str, ttype: str, priority: int, flags: str) -> Task:
        '''update is used to update task

        Args:
            tid (str): id of the task
            fid (str): id of associated feature
            aid (str): id of associated assignee
            name (str): name of the task
            description (str): description of the task
            status (str): status of the task, for example
                'in progress', 'waiting', 'ready', 'postponed'
            ttype (str): type of the task, for example
                'new feature', 'bug fixes'
            priority (int): priority of the task, in three stages:
                low, medium and high (1 = low, 3 = high)
            flags (str): flags used to identify tasks,
                given in string, example = 'one;two;flags;'

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database
            EmptyValueException: raised if any given values is empty
            UnvalidInputException: raised if formatting of given
                input value is incorrect
            NotExistingException: raised if feature, feature owner or project
                with given id is not found

        Returns:
            Task: updated task
        '''
        if (not tid or not fid or not aid or not name or not description
                or not status or not ttype or not priority):
            raise EmptyValueException(
                'One of given values is empty, all values need to have value')

        if not validate_uuid4(tid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='task id')

        self._task_repository.get_by_id(tid)

        if not validate_uuid4(fid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='feature id')
        if not validate_uuid4(aid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='assignee')
        if not validate_uuid4(ttype):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='task type id')
        if not validate_uuid4(status):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='status id')

        if not validate_flags(flags):
            raise UnvalidInputException(
                'Unvalid formatting',
                'not being in "one;two;three;flags;" format', 'flags')

        try:
            priority = int(priority)
        except Exception as error:
            raise UnvalidInputException(
                reason='can not be converted into integer',
                source='priority') from error

        if not 1 <= priority <= 3:
            raise UnvalidInputException(reson='priority is not in scale 1-3',
                                        source='priority')

        fname = self._feature_repository.get_name(fid)
        aname = self._user_repository.get_fullname(aid)
        sname = self._status_service.get_name(status)
        ttname = self._type_service.get_name(ttype)

        if not fname:
            raise NotExistingException('Feature')
        if not aname:
            raise NotExistingException('Assignee')
        if not sname:
            raise NotExistingException('Status')
        if not ttname:
            raise NotExistingException('Type')

        task_id, created, updated_on = self._task_repository.update(
            fid, aid, name, description, status, ttype, priority, flags)

        updated_task = Task(task_id, fid, fname, aid, aname, name, description,
                            status, sname, ttype, ttname, priority, created,
                            updated_on, flags)
        return updated_task

    def remove(self, tid: str) -> None:
        '''remove is used to remove task from the database

        Args:
            tid (str): id of the task to be removed

        Raises:
            DatabaseException: raised if problems occurs
                while interacting with database.
            NotExistingException: raised if feature not found with given id
            UnvalidInputException: raised if unvalid
                id is given
        '''

        if not validate_uuid4(tid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='task id')

        self._task_repository.get_by_id(tid)
        self._task_repository.remove(tid)


task_service = TaskService()
