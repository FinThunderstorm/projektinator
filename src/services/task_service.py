from repositories.feature_repository import FeatureRepository
from repositories.task_repository import task_repository, TaskRepository
from entities.task import Task
from repositories.user_repository import UserRepository, user_repository
from repositories.task_repository import TaskRepository, task_repository
from repositories.feature_repository import FeatureRepository, feature_repository
from utils.exceptions import EmptyValueException, NotExistingException, UnvalidInputException
from utils.validators import validate_flags, validate_uuid4


class TaskService:
    """Class used for handling users in the application
    """

    def __init__(
            self,
            default_task_repository: TaskRepository = task_repository,
            default_feature_repository: FeatureRepository = feature_repository,
            default_user_repository: UserRepository = user_repository):
        """Initializes TaskService with default task repository

        Args:
            default_task_repository (TaskRepository, optional): option to give custom task_repository. Defaults to task_repository.
        """
        self._task_repository = default_task_repository
        self._feature_repository = default_feature_repository
        self._user_repository = default_user_repository

    def new(self,
            fid: str,
            aid: str,
            name: str,
            description: str,
            status: str,
            ttype: str,
            priority: int,
            flags: str = "") -> Task:
        """new is used to create new tasks

        Args:
            fid (str): id of associated feature
            aid (str): id of associated assignee
            name (str): name of task
            description (str): description of task
            status (str): status of task, for example "in progress", "waiting", "ready", "postponed"
            ttype (str): type of task, for example "new feature", "bug fixes"
            priority (int): priority of task, in three stages: low, severe and high (1 = low, 3 = high)
            flags (str, optional): flags used to identify tasks, given in string, example = "one;two;flags;". Defaults to "".

        Raises:
            DatabaseException: raised if problems occurs while saving into the database
            EmptyValueException: raised if any given values is empty
            UnvalidInputException: raised if formatting of given input value is incorrect
            NotExistingException: raised if feature owner or project with given id is not found

        Returns:
            Task: created task
        """
        if not fid or not aid or not name or not description or not status or not ttype or not priority:
            raise EmptyValueException(
                'One of given values is empty, all values need to have value')

        if not validate_uuid4(fid):
            raise UnvalidInputException(reason="unvalid formatting of uuid4",
                                        source="feature id")

        if not validate_uuid4(aid):
            raise UnvalidInputException(reason="unvalid formatting of uuid4",
                                        source="assignee")

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

        fname = self._feature_repository.get_name(fid)
        aname = self._user_repository.get_fullname(aid)

        if not fname:
            raise NotExistingException('Feature')
        if not aname:
            raise NotExistingException('Assignee')

        created_task = self._task_repository.new(fid, fname, aid, aname, name,
                                                 description, status, ttype,
                                                 priority, flags)
        return created_task

    def get_all(self) -> [Task]:
        """get_all is used to get all tasks from the database

        Raises:
            DatabaseException: raised if problem occurs while interacting with the database
            NotExistingException: raised if features not found

        Returns:
            [Task]: list of all found tasks
        """
        tasks = self._task_repository.get_all()
        if not tasks:
            raise NotExistingException('Features', 'not found')
        return tasks

    def get_all_by_feature_id(self, fid: str) -> [Task]:
        """get_all_by_feature_id is used to find all tasks associated with given feature

        Args:
            fid (str): if of feature associated with

        Raises:
            DatabaseException: raised if problem occurs while interacting with the database
            NotExistingException: raised if feature or tasks not found

        Returns:
            [Task]: list of all found tasks
        """
        if not self._feature_repository.get_by_id(fid):
            raise NotExistingException('Feature')

        tasks = self._task_repository.get_all_by_feature_id(fid)

        if not tasks:
            raise NotExistingException('Tasks')

        return tasks

    def get_all_by_assignee(self, aid: str) -> [Task]:
        """get_all_by_assignee is used to find all tasks associated with given assignee

        Args:
            aid (str): if of assignee associated with

        Raises:
            DatabaseException: raised if problem occurs while interacting with the database
            NotExistingException: raised if assignee or tasks not found

        Returns:
            [Task]: list of all found tasks
        """
        if not self._user_repository.get_by_id(aid):
            raise NotExistingException('Assignee')

        tasks = self._task_repository.get_all_by_assignee(aid)

        if not tasks:
            raise NotExistingException('Tasks')

        return tasks

    def get_by_id(self, tid: str) -> Task:
        """get_by_id is used to find specific task

        Args:
            tid (str): if of task to be found

        Raises:
            DatabaseException: raised if problems occur while interacting with the database

        Returns:
            Task: found task
        """
        task = self._task_repository.get_by_id(tid)

        if not task:
            raise NotExistingException('Task')

        return task

    def get_name(self, tid: str) -> str:
        """get_name is used to get name of specific task

        Args:
            tid (str): if of task

        Raises:
            DatabaseException: raised if problems occur while interacting with the database
            NotExistingException: raised if task not found with given id

        Returns:
            str: found name
        """
        name = self._task_repository.get_name()

        if not name:
            raise NotExistingException('Task')

        return name

    def update(self, tid: str, fid: str, aid: str, name: str, description: str,
               status: str, ttype: str, priority: int, flags: str) -> Task:
        """update is used to update tasks

        Args:
            tid (str): id of task to be updated
            fid (str): id of associated feature
            aid (str): id of associated assignee
            name (str): name of task
            description (str): description of task
            status (str): status of task, for example "in progress", "waiting", "ready", "postponed"
            ttype (str): type of task, for example "new feature", "bug fixes"
            priority (int): priority of task, in three stages: low, severe and high (1 = low, 3 = high)
            flags (str): flags used to identify tasks, given in string, example = "one;two;flags;".

        Raises:
            DatabaseException: raised if problems occurs while saving into the database
            EmptyValueException: raised if any given values is empty
            UnvalidInputException: raised if formatting of given input value is incorrect
            NotExistingException: raised if task, feature owner or project with given id is not found

        Returns:
            Task: updated task
        """
        if not tid or not fid or not aid or not name or not description or not status or not ttype or not priority:
            raise EmptyValueException(
                'One of given values is empty, all values need to have value')

        task = self._task_repository.get_by_id(tid)
        if not task:
            raise NotExistingException('Task')

        if not validate_uuid4(fid):
            raise UnvalidInputException(reason="unvalid formatting of uuid4",
                                        source="feature id")

        if not validate_uuid4(aid):
            raise UnvalidInputException(reason="unvalid formatting of uuid4",
                                        source="assignee")

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

        fname = self._feature_repository.get_name(fid)
        aname = self._user_repository.get_fullname(aid)

        if not fname:
            raise NotExistingException('Feature')
        if not aname:
            raise NotExistingException('Assignee')

        updated_task = self._task_repository.update(tid, fid, fname, aid, aname,
                                                    name, description, status,
                                                    ttype, priority, flags)
        return updated_task

    def remove(self, tid: str) -> None:
        """remove is used to remove task from the database

        Args:
            tid (str): id of task

        Raises:
            DatabaseException: raised if problems occur while interacting with the database
            NotExistingException: raised if task not found
        """
        if not self._task_repository.get_by_id(tid):
            raise NotExistingException('Task')
        self._task_repository.remove(tid)


task_service = TaskService()
