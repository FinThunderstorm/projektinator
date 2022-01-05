from entities.comment import Comment
from utils.database import db
from utils.exceptions import DatabaseException, NotExistingException
from utils.helpers import fullname


class CommentRepository:
    '''Class used for handling comments in the database
    '''

    def new(self,
            aid: str,
            comment: str,
            tspent: float,
            tid: str = None,
            fid: str = None) -> tuple:
        """new is used to create new comments into the database

        Args:
            aid (str): id of the comments's assignee
            comment (str): content of the comment
            tspent (float): time spent, used for time tracking
            tid (str, optional): id of the related task. Defaults to None.
            fid (str, optional): id of the related feature. Defaults to None.

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database

        Returns:
            tuple: created comment's id, creation and updated on
        """

        values = {
            'feature_id': fid,
            'task_id': tid,
            'comment': comment,
            'time_spent': tspent,
            'assignee': aid,
        }

        sql_feature = '''
            INSERT INTO Comments
            (feature_id, comment, time_spent, assignee)
            VALUES (:feature_id, :comment, :time_spent, :assignee)
            RETURNING id, created, updated_on
        '''

        sql_task = '''
            INSERT INTO Comments
            (task_id, comment, time_spent, assignee)
            VALUES (:task_id, :comment, :time_spent, :assignee)
            RETURNING id, created, updated_on
        '''

        sql = sql_feature if fid else sql_task

        try:
            cid, created, updated_on = db.session.execute(sql,
                                                          values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException('While saving new comment') from error

        if not cid:
            raise DatabaseException('While saving new comment') from error

        return (cid, created, updated_on)

    def get_by_id(self, cid: str) -> tuple:
        """get_by_id is used to find exact comment with
           given id from the database

        Args:
            cid (str): id of the comment to be found

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if there is none comments with given id

        Returns:
            tuple: comment with given id
        """

        sql = '''
            SELECT C.id, C.assignee, U.firstname, U.lastname, C.time_spent, C.comment, C.created, C.updated_on, C.feature_id, F.name, C.task_id, T.name  
            FROM Comments C
            LEFT JOIN Users U ON C.assignee = U.id
            LEFT JOIN Features F ON C.feature_id = F.id
            LEFT JOIN Tasks T ON C.task_id = T.id
            WHERE C.id=:id
        '''

        try:
            comment = db.session.execute(sql, {'id': cid}).fetchone()
        except Exception as error:
            raise DatabaseException('While getting the comment') from error

        if not comment:
            raise NotExistingException('Comment')

        if comment[8]:
            return ('features', comment[0], comment[1], comment[2], comment[3],
                    comment[4], comment[5], comment[6], comment[7], comment[8],
                    comment[9])
        elif comment[10]:
            return ('tasks', comment[0], comment[1], comment[2], comment[3],
                    comment[4], comment[5], comment[6], comment[7], comment[10],
                    comment[11])
        else:
            raise NotExistingException('Comment')

    def get_all_by_feature_id(self, fid: str) -> [tuple]:
        """get_all_by_feature_id is used to get list of all comments
           associated with given feature id in the database.

           If no comments found, returns empty list.

        Args:
            fid (str): id of the related feature

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of found comments
        """

        sql = '''
            SELECT C.id, C.assignee, U.firstname, U.lastname, C.time_spent, C.comment, C.created, C.updated_on, C.feature_id, F.name, C.task_id, T.name
            FROM Comments C
            JOIN Users U ON C.assignee = U.id
            JOIN Features F ON C.feature_id = F.id
            WHERE C.feature_id=:id
        '''

        try:
            comments = db.session.execute(sql, {'id': fid}).fetchall()
        except Exception as error:
            raise DatabaseException('While getting all comments') from error

        return [('features', comment[0], comment[1], comment[2], comment[3],
                 comment[4], comment[5], comment[6], comment[7], comment[8],
                 comment[9]) for comment in comments]

    def get_all_by_task_id(self, tid: str) -> [tuple]:
        """get_all_by_task_id is used to get list of all comments
           associated with given task id in the database.

           If no comments found, returns empty list.

        Args:
            tid (str): id of the related task

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of found comments
        """

        sql = '''
            SELECT C.id, C.assignee, U.firstname, U.lastname, C.time_spent, C.comment, C.created, C.updated_on, C.feature_id, F.name, C.task_id, T.name
            FROM Comments C
            JOIN Users U ON C.assignee = U.id
            JOIN Tasks T ON C.task_id = T.id
            WHERE C.task_id=:id
        '''

        try:
            comments = db.session.execute(sql, {'id': tid}).fetchall()
        except Exception as error:
            raise DatabaseException('While getting all comments') from error

        return [('tasks', comment[0], comment[1], comment[2], comment[3],
                 comment[4], comment[5], comment[6], comment[7], comment[10],
                 comment[11]) for comment in comments]

    def get_all_by_assignee(self, aid: str) -> [tuple]:
        """get_all_by_assignee is used to get list of all comments
           associated with given assignee's id in the database.

           If no comments found, returns empty list.

        Args:
            aid (str): id of the related assignee

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of found comments
        """

        sql = '''
            SELECT C.id, C.assignee, U.firstname, U.lastname, C.time_spent, C.comment, C.created, C.updated_on, C.feature_id, F.name, C.task_id, T.name
            FROM Comments C
            JOIN Users U ON C.assignee = U.id
            JOIN Features F ON C.feature_id = F.id
            JOIN Tasks T ON C.task_id = T.id
            WHERE C.assignee=:id
        '''
        try:
            comments = db.session.execute(sql, {'id': aid}).fetchall()
        except Exception as error:
            raise DatabaseException('While getting all comments') from error

        return [('features', comment[0], comment[1], comment[2], comment[3],
                 comment[4], comment[5], comment[6], comment[7], comment[8],
                 comment[9]) if comment[8] else
                ('tasks', comment[0], comment[1], comment[2], comment[3],
                 comment[4], comment[5], comment[6], comment[7], comment[10],
                 comment[11]) for comment in comments]

    def update(self,
               cid: str,
               aid: str,
               comment_text: str,
               tspent: float,
               tid: str = None,
               fid: str = None) -> tuple:
        """update is used to update new values into
           the database for specific comment

        Args:
            cid (str): id of the comment
            aid (str): id of the comments's assignee
            aname (str): name of the comments's assignee
            comment (str): content of the comment
            tspent (float): time spent, used for time tracking
            tid (str, optional): id of the related task. Defaults to None.
            tname (str, optional): name of the related task. Defaults to None.
            fid (str, optional): id of the related feature. Defaults to None.
            fname (str, optional): name of the related feature.
                Defaults to None.

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database

        Returns:
            tuple: updated comment's id, creation and updated on
        """

        values = {
            'id': cid,
            'feature_id': fid,
            'task_id': tid,
            'comment': comment_text,
            'time_spent': tspent,
            'assignee': aid,
        }

        sql_feature = '''
            UPDATE Comments 
            SET feature_id=:feature_id, comment=:comment, time_spent=:time_spent, assignee=:assignee 
            WHERE id=:id 
            RETURNING id, created, updated_on
        '''

        sql_task = '''
            UPDATE Comments 
            SET task_id=:task_id, comment=:comment, time_spent=:time_spent, assignee=:assignee 
            WHERE id=:id 
            RETURNING id, created, updated_on
        '''

        sql = sql_feature if fid else sql_task

        try:
            comment_id, created, updated_on = db.session.execute(
                sql, values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException('While saving updated comment') from error

        if str(cid) != str(comment_id):
            raise DatabaseException('While saving updated comment') from error

        return (cid, created, updated_on)

    def remove(self, cid: str):
        """remove is used to remove comment from the database

        Args:
            cid (str): id of comment to be removed

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
        """

        sql = '''
            DELETE FROM Comments 
            WHERE id=:id
        '''

        try:
            db.session.execute(sql, {'id': cid})
            db.session.commit()
        except Exception as error:
            raise DatabaseException('While removing the comment') from error


comment_repository = CommentRepository()
