from entities.task import Task

from utils.database import db

from datetime import datetime
from utils.exceptions import DatabaseException
from utils.helpers import fullname


class TaskRepository:
    """Class used for handling tasks in the database
    """

    def new(self, fid: str, fname: str, aid: str, aname: str, name: str, description: str, status: str, ttype: str, priority: int, flags: str) -> Task:
        """new is used to create new tasks into the database

        Args:
            fid (str): id of associated feature
            fname (str): name of associated feature
            aid (str): id of associated assignee
            aname (str): name of associated assignee
            name (str): name of task
            description (str): description of task
            status (str): status of task, for example "in progress", "waiting", "ready", "postponed"
            ttype (str): type of task, for example "new feature", "bug fixes"
            priority (int): priority of task, in three stages: low, severe and high (1 = low, 3 = high)
            flags (str): flags used to identify tasks, given in string, example = "one;two;flags;"

        Raises:
            DatabaseException: raised if problems occurs while saving into the database

        Returns:
            Task: created task as Task object
        """
        values = {
            "feature_id": fid,
            "assignee": aid,
            "name": name,
            "description": description,
            "flags": flags,
            "status": status,
            "type": ttype,
            "priority": priority
        }
        sql = """
        INSERT INTO Tasks
        (feature_id, assignee, name, description, flags, status, type, priority) 
        VALUES (:feature_id, :assignee, :name, :description, :flags, :status, :type, :priority) 
        RETURNING id, created, updated_on
        """
        try:
            tid, created, updated_on = db.session.execute(
                sql, values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException(
                'While ssaving new task into database') from error

        if not tid:
            raise DatabaseException('While saving new task into database')

        created_task = Task(tid, fid, fname, aid, aname, name, description,
                            status, ttype, priority, created, updated_on, flags)
        return created_task

    def get_all(self) -> [Task]:
        """get_all is used to get all tasks from the database

        Raises:
            DatabaseException: raised if problem occurs while interacting with the database

        Returns:
            [Task]: list of all found tasks
        """
        sql = """
        SELECT T.id, T.feature_id, F.name, T.assignee, U.firstname, U.lastname, T.name, T.description, T.flags, T.status, T.type, T.priority, T.created, T.updated_on
        FROM Tasks T
        JOIN Features F ON F.id = T.feature_id
        JOIN Users U ON U.id = T.assignee
        """
        try:
            tasks = db.session.execute(sql).fetchall()
        except Exception as error:
            raise DatabaseException('while getting all tasks') from error

        all_comments = None

        return [Task(task[0], task[1], task[2], task[3], fullname(task[4], task[5]), task[6], task[7], task[9], task[10], task[11], task[12], task[13], task[8], all_comments) for task in tasks]

    def get_all_by_feature_id(self, fid: str) -> [Task]:
        """get_all_by_feature_id is used to find all tasks associated with given feature

        Args:
            fid (str): if of feature associated with

        Raises:
            DatabaseException: raised if problem occurs while interacting with the database

        Returns:
            [Task]: list of all found tasks
        """
        sql = """
        SELECT T.id, T.feature_id, F.name, T.assignee, U.firstname, U.lastname, T.name, T.description, T.flags, T.status, T.type, T.priority, T.created, T.updated_on
        FROM Tasks T
        JOIN Features F ON F.id = T.feature_id
        JOIN Users U ON U.id = T.assignee
        WHERE T.feature_id=:id
        """
        try:
            tasks = db.session.execute(sql, {"id": fid}).fetchall()
        except Exception as error:
            raise DatabaseException('while getting all tasks') from error

        all_comments = None

        return [Task(task[0], task[1], task[2], task[3], fullname(task[4], task[5]), task[6], task[7], task[9], task[10], task[11], task[12], task[13], task[8], all_comments) for task in tasks]

    def get_all_by_assignee(self, aid: str) -> [Task]:
        """get_all_by_assignee is used to find all tasks associated with given assignee

        Args:
            aid (str): if of assignee associated with

        Raises:
            DatabaseException: raised if problem occurs while interacting with the database

        Returns:
            [Task]: list of all found tasks
        """
        sql = """
        SELECT T.id, T.feature_id, F.name, T.assignee, U.firstname, U.lastname, T.name, T.description, T.flags, T.status, T.type, T.priority, T.created, T.updated_on
        FROM Tasks T
        JOIN Features F ON F.id = T.feature_id
        JOIN Users U ON U.id = T.assignee
        WHERE T.assignee=:id
        """
        try:
            tasks = db.session.execute(sql, {"id": aid}).fetchall()
        except Exception as error:
            raise DatabaseException('while getting all tasks') from error

        all_comments = None

        return [Task(task[0], task[1], task[2], task[3], fullname(task[4], task[5]), task[6], task[7], task[9], task[10], task[11], task[12], task[13], task[8], all_comments) for task in tasks]

    def get_by_id(self, tid: str) -> Task:
        """get_by_id is used to find specific task

        Args:
            tid (str): if of task to be found

        Raises:
            DatabaseException: raised if problems occur while interacting with the database

        Returns:
            Task: found task
        """
        sql = """
        SELECT T.id, T.feature_id, F.name, T.assignee, U.firstname, U.lastname, T.name, T.description, T.flags, T.status, T.type, T.priority, T.created, T.updated_on
        FROM Tasks T
        JOIN Features F ON F.id = T.feature_id
        JOIN Users U ON U.id = T.assignee
        WHERE T.id=:id
        """
        try:
            task = db.session.execute(sql, {"id": tid}).fetchone()
        except Exception as error:
            raise DatabaseException('while getting all tasks') from error

        all_comments = None

        return Task(task[0], task[1], task[2], task[3], fullname(task[4], task[5]), task[6], task[7], task[9], task[10], task[11], task[12], task[13], task[8], all_comments)

    def get_name(self, tid: str) -> str:
        """get_name is used to get name of specific task

        Args:
            tid (str): if of task

        Raises:
            DatabaseException: raised if problems occur while interacting with the database

        Returns:
            str: found name
        """
        sql = """
        SELECT name
        FROM Tasks
        WHERE id=:id
        """
        try:
            name = db.session.execute(sql, {"id": tid}).fetchone()
        except Exception as error:
            raise DatabaseException('while getting all tasks') from error

        return name

    def update(self, tid: str, fid: str, fname: str, aid: str, aname: str, name: str, description: str, status: str, ttype: str, priority: int, flags: str) -> Task:
        """update is used to update task in the database

        Args:
            tid (str): id of task
            fid (str): id of associated feature
            fname (str): name of associated feature
            aid (str): id of associated assignee
            aname (str): name of associated assignee
            name (str): name of task
            description (str): description of task
            status (str): status of task, for example "in progress", "waiting", "ready", "postponed"
            ttype (str): type of task, for example "new feature", "bug fixes"
            priority (int): priority of task, in three stages: low, severe and high (1 = low, 3 = high)
            flags (str): flags used to identify tasks, given in string, example = "one;two;flags;"

        Raises:
            DatabaseException: raised if problems occur while interacting with the database


        Returns:
            Task: updated task as Task object
        """
        sql = """
        UPDATE Tasks
        SET feature_id=:feature_id, assignee=:assignee, name=:name, description=:description, flags=:flags, status=:status, type=:type, priority=:priority
        WHERE id=:id
        RETURNING created, updated_on
        """
        values = {
            "feature_id": fid,
            "assignee": aid,
            "name": name,
            "description": description,
            "flags": flags,
            "status": status,
            "type": ttype,
            "priority": priority
        }
        try:
            created, updated_on = db.session.execute(
                sql, values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException(
                'While ssaving new task into database') from error

        if not tid:
            raise DatabaseException('While saving updated task into database')

        all_comments = None

        updated_task = Task(tid, fid, fname, aid, aname, name, description,
                            status, ttype, priority, created, updated_on, flags, all_comments)
        return updated_task

    def remove(self, tid: str) -> None:
        """remove is used to remove task from the database

        Args:
            tid (str): id of task

        Raises:
            DatabaseException: raised if problems occur while interacting with the database
        """
        sql = "DELETE FROM Tasks WHERE id=:id"
        try:
            db.session.execute(sql, {"id": tid})
            db.session.commit()
        except Exception as error:
            raise DatabaseException('while removing task') from error


task_repository = TaskRepository()
