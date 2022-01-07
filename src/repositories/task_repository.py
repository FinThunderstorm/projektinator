from utils.database import db
from utils.exceptions import DatabaseException, NotExistingException


class TaskRepository:
    '''Class used for handling tasks in the database
    '''

    def new(self, fid: str, aid: str, name: str, description: str, status: str,
            ttype: str, priority: int, flags: str) -> tuple:
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

        Returns:
            tuple: created task´s id, creation and updated on time
        '''

        values = {
            'feature_id': fid,
            'assignee': aid,
            'name': name,
            'description': description,
            'flags': flags,
            'status': status,
            'type': ttype,
            'priority': priority
        }

        sql = '''
            INSERT INTO Tasks
            (feature_id, assignee, name, description, flags, status, type, priority) 
            VALUES (:feature_id, :assignee, :name, :description, :flags, :status, :type, :priority) 
            RETURNING id, created, updated_on
        '''

        try:
            task_id, created, updated_on = db.session.execute(
                sql, values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException(
                'While ssaving new task into database') from error

        if not task_id:
            raise DatabaseException('While saving new task into database')

        return (task_id, created, updated_on)

    def get_all(self) -> [tuple]:
        '''get_all is used to get all tasks from the database

        If no tasks found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of all tasks
        '''

        sql = '''
            SELECT T.id, T.feature_id, F.name, T.assignee, U.firstname, U.lastname, T.name, T.description, T.status, S.name, T.type, Ty.name, T.priority, T.created, T.updated_on, T.flags
            FROM Tasks T
            JOIN Features F ON F.id = T.feature_id
            JOIN Users U ON U.id = T.assignee
            JOIN Types Ty ON Ty.id = T.type
            JOIN Statuses S ON S.id = T.status
        '''

        try:
            tasks = db.session.execute(sql).fetchall()
        except Exception as error:
            raise DatabaseException('While getting all tasks') from error

        return [(task[0], task[1], task[2], task[3], task[4], task[5], task[6],
                 task[7], task[8], task[9], task[10], task[11], task[12],
                 task[13], task[14], task[15]) for task in tasks]

    def get_all_by_feature_id(self, fid: str) -> [tuple]:
        '''get_all_by_feature_id is used to get all tasks
           associated with given task

        If no tasks found, returns empty list.

        Args:
            fid (str): id of the feature in which tasks are associated

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of found tasks
        '''

        sql = '''
            SELECT T.id, T.feature_id, F.name, T.assignee, U.firstname, U.lastname, T.name, T.description, T.status, S.name, T.type, Ty.name, T.priority, T.created, T.updated_on, T.flags
            FROM Tasks T
            JOIN Features F ON F.id = T.feature_id
            JOIN Users U ON U.id = T.assignee
            JOIN Types Ty ON Ty.id = T.type
            JOIN Statuses S ON S.id = T.status
            WHERE T.feature_id=:id
        '''

        try:
            tasks = db.session.execute(sql, {'id': fid}).fetchall()
        except Exception as error:
            raise DatabaseException(
                'While getting all tasks by Feature ID') from error

        return [(task[0], task[1], task[2], task[3], task[4], task[5], task[6],
                 task[7], task[8], task[9], task[10], task[11], task[12],
                 task[13], task[14], task[15]) for task in tasks]

    def get_all_by_assignee(self, aid: str) -> [tuple]:
        '''get_all_by_feature_id is used to get all tasks
           associated with given task

        If no tasks found, returns empty list.

        Args:
            fid (str): id of the feature in which tasks are associated

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of found tasks
        '''

        sql = '''
            SELECT T.id, T.feature_id, F.name, T.assignee, U.firstname, U.lastname, T.name, T.description, T.status, S.name, T.type, Ty.name, T.priority, T.created, T.updated_on, T.flags
            FROM Tasks T
            JOIN Features F ON F.id = T.feature_id
            JOIN Users U ON U.id = T.assignee
            JOIN Types Ty ON Ty.id = T.type
            JOIN Statuses S ON S.id = T.status
            WHERE T.assignee=:id
        '''

        try:
            tasks = db.session.execute(sql, {'id': aid}).fetchall()
        except Exception as error:
            raise DatabaseException(
                'While getting all tasks by assignee') from error

        return [(task[0], task[1], task[2], task[3], task[4], task[5], task[6],
                 task[7], task[8], task[9], task[10], task[11], task[12],
                 task[13], task[14], task[15]) for task in tasks]

    def get_by_id(self, tid: str) -> tuple:
        '''get_by_id is used to found task with given id

        Args:
            tid (str): id of the task

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if there is none tasks with given id

        Returns:
            tuple: found task
        '''

        sql = '''
            SELECT T.id, T.feature_id, F.name, T.assignee, U.firstname, U.lastname, T.name, T.description, T.status, S.name, T.type, Ty.name, T.priority, T.created, T.updated_on, T.flags
            FROM Tasks T
            JOIN Features F ON F.id = T.feature_id
            JOIN Users U ON U.id = T.assignee
            JOIN Types Ty ON Ty.id = T.type
            JOIN Statuses S ON S.id = T.status
            WHERE T.id=:id
        '''

        try:
            task = db.session.execute(sql, {'id': tid}).fetchone()
        except Exception as error:
            raise DatabaseException('While getting the task') from error

        if not task:
            raise NotExistingException('Task')

        return (task[0], task[1], task[2], task[3], task[4], task[5], task[6],
                task[7], task[8], task[9], task[10], task[11], task[12],
                task[13], task[14], task[15])

    def get_name(self, tid: str) -> str:
        '''get_name is used to get name of specific task

        Args:
            tid (str): if of the task

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if feature is not
                found with given id

        Returns:
            str: found name
        '''

        sql = '''
            SELECT name
            FROM Tasks
            WHERE id=:id
        '''

        try:
            name = db.session.execute(sql, {'id': tid}).fetchone()
        except Exception as error:
            raise DatabaseException('While getting task´s name') from error

        if not name:
            raise NotExistingException('Task')

        return name[0]

    def update(self, tid: str, fid: str, aid: str, name: str, description: str,
               status: str, ttype: str, priority: int, flags: str) -> tuple:
        '''update is used to update task in the database

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

        Returns:
            tuple: updated task´s id, creation and updated on time
        '''

        sql = '''
            UPDATE Tasks
            SET feature_id=:feature_id, assignee=:assignee, name=:name, description=:description, flags=:flags, status=:status, type=:type, priority=:priority
            WHERE id=:id
            RETURNING id, created, updated_on
        '''

        values = {
            'id': tid,
            'feature_id': fid,
            'assignee': aid,
            'name': name,
            'description': description,
            'flags': flags,
            'status': status,
            'type': ttype,
            'priority': priority
        }

        try:
            task_id, created, updated_on = db.session.execute(
                sql, values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException('While saving updated task') from error

        if str(tid) != str(task_id):
            raise DatabaseException('While saving updated task')

        return (task_id, created, updated_on)

    def remove(self, tid: str) -> None:
        '''remove is used to remove task from the database

        Args:
            fid (str): id of the task to be removed

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
        '''

        sql = '''
            DELETE FROM Tasks 
            WHERE id=:id
        '''

        try:
            db.session.execute(sql, {'id': tid})
            db.session.commit()
        except Exception as error:
            raise DatabaseException('While removing the task') from error


task_repository = TaskRepository()
