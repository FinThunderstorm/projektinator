from datetime import datetime

from entities.comment import Comment
from utils.database import db
from utils.exceptions import DatabaseException, NotExistingException
from utils.helpers import fullname


class CommentRepository:
    """Class used for handling comments in the database
    """

    def new(self,
            aid: str,
            aname: str,
            comment: str,
            tspent: float,
            tid: str = None,
            tname: str = None,
            fid: str = None,
            fname: str = None):

        values = {
            "feature_id": fid,
            "task_id": tid,
            "comment": comment,
            "time_spent": tspent,
            "assignee": aid,
        }
        sql_feature = """
        INSERT INTO Comments
        (feature_id, comment, time_spent, assignee)
        VALUES (:feature_id, :comment, :time_spent, :assignee)
        RETURNING id, created, updated_on
        """
        sql_task = """
        INSERT INTO Comments
        (task_id, comment, time_spent, assignee)
        VALUES (:task_id, :comment, :time_spent, :assignee)
        RETURNING id, created, updated_on
        """
        sql = sql_feature if fid != None else sql_task

        try:
            cid, created, updated_on = db.session.execute(sql,
                                                          values).fetchone()
            db.session.commit()
        except Exception as error:
            print(error)
            raise DatabaseException(
                'While saving new comment into database') from error

        if not cid:
            raise DatabaseException(
                'While saving new comment into database') from error

        if fid != None:
            created_comment = Comment(cid,
                                      aid,
                                      aname,
                                      tspent,
                                      comment,
                                      created,
                                      updated_on,
                                      fid=fid,
                                      fname=fname)
            return created_comment
        else:
            created_comment = Comment(cid,
                                      aid,
                                      aname,
                                      tspent,
                                      comment,
                                      created,
                                      updated_on,
                                      tid=tid,
                                      tname=tname)
            return created_comment

    def get_by_id(self, cid: str):
        sql = """
        SELECT C.id, C.feature_id, F.name, C.task_id, T.name, C.comment, C.time_spent, C.assignee, U.firstname, U.lastname, C.created, C.updated_on
        FROM Comments C
        JOIN Users U ON C.assignee = U.id
        JOIN Features F ON C.feature_id = F.id
        JOIN Tasks T ON C.task_id = T.id
        WHERE C.id=:id
        """
        try:
            comment = db.session.execute(sql, {"id": cid}).fetchone()
        except Exception as error:
            raise DatabaseException('while getting all projects') from error

        return Comment(comment[0],
                       comment[7],
                       fullname(comment[8], comment[9]),
                       comment[6],
                       comment[5],
                       comment[10],
                       comment[11],
                       fid=comment[1],
                       fname=comment[2]) if comment[1] != None else Comment(
                           comment[0],
                           comment[7],
                           fullname(comment[8], comment[9]),
                           comment[6],
                           comment[5],
                           comment[10],
                           comment[11],
                           tid=comment[3],
                           tname=comment[4])

    def get_by_feature_id(self, fid: str):
        sql = """
        SELECT C.id, C.feature_id, F.name, C.comment, C.time_spent, C.assignee, U.firstname, U.lastname, C.created, C.updated_on
        FROM Comments C
        JOIN Users U ON C.assignee = U.id
        JOIN Features F ON C.feature_id = F.id
        WHERE C.feature_id=:id
        """
        try:
            comments = db.session.execute(sql, {"id": fid}).fetchall()
        except Exception as error:
            print(error)
            raise DatabaseException('while getting all comments') from error

        return [
            Comment(comment[0],
                    comment[5],
                    fullname(comment[6], comment[7]),
                    comment[4],
                    comment[3],
                    comment[8],
                    comment[9],
                    fid=comment[1],
                    fname=comment[2]) for comment in comments
        ]

    def get_by_task_id(self, tid: str):
        sql = """
        SELECT C.id, C.task_id, T.name, C.comment, C.time_spent, C.assignee, U.firstname, U.lastname, C.created, C.updated_on
        FROM Comments C
        JOIN Users U ON C.assignee = U.id
        JOIN Tasks T ON C.task_id = T.id
        WHERE C.task_id=:id
        """
        try:
            comments = db.session.execute(sql, {"id": tid}).fetchall()
        except Exception as error:
            raise DatabaseException('while getting all projects') from error

        return [
            Comment(comment[0],
                    comment[5],
                    fullname(comment[6], comment[7]),
                    comment[4],
                    comment[3],
                    comment[8],
                    comment[9],
                    tid=comment[1],
                    tname=comment[2]) for comment in comments
        ]

    def get_by_assignee(self, aid: str):
        sql = """
        SELECT C.id, C.feature_id, F.name, C.task_id, T.name, C.comment, C.time_spent, C.assignee, U.firstname, U.lastname, C.created, C.updated_on
        FROM Comments C
        JOIN Users U ON C.assignee = U.id
        JOIN Features F ON C.feature_id = F.id
        JOIN Tasks T ON C.task_id = T.id
        WHERE C.assignee=:id
        """
        try:
            comments = db.session.execute(sql, {"id": aid}).fetchall()
        except Exception as error:
            raise DatabaseException('while getting all projects') from error

        return [
            Comment(comment[0],
                    comment[7],
                    fullname(comment[8], comment[9]),
                    comment[6],
                    comment[5],
                    comment[10],
                    comment[11],
                    fid=comment[1],
                    fname=comment[2])
            if comment[1] != None else Comment(comment[0],
                                               comment[7],
                                               fullname(comment[8], comment[9]),
                                               comment[6],
                                               comment[5],
                                               comment[10],
                                               comment[11],
                                               tid=comment[3],
                                               tname=comment[4])
            for comment in comments
        ]

    def update(self,
               cid: str,
               aid: str,
               aname: str,
               comment: str,
               tspent: float,
               tid: str = None,
               tname: str = None,
               fid: str = None,
               fname: str = None):
        values = {
            "id": cid,
            "feature_id": fid,
            "task_id": tid,
            "comment": comment,
            "time_spent": tspent,
            "assignee": aid,
        }
        sql_feature = """
        UPDATE Comments 
        SET feature_id=:feature_id, comment=:comment, time_spent=:time_spent, assignee=:assignee 
        WHERE id=:id 
        RETURNING id, created, updated_on
        """
        sql_task = """
        UPDATE Comments 
        SET task_id=:task_id, comment=:comment, time_spent=:time_spent, assignee=:assignee 
        WHERE id=:id 
        RETURNING id, created, updated_on
        """
        sql = sql_feature if fid != None else sql_task
        try:
            comment_id, created, updated_on = db.session.execute(
                sql, values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException(
                'While saving updated comment into database') from error

        if str(cid) != str(comment_id):
            raise DatabaseException(
                'While saving new comment into database') from error

        if fid != None:
            created_comment = Comment(cid,
                                      aid,
                                      aname,
                                      tspent,
                                      comment,
                                      created,
                                      updated_on,
                                      fid=fid,
                                      fname=fname)
            return created_comment
        else:
            created_comment = Comment(cid,
                                      aid,
                                      aname,
                                      tspent,
                                      comment,
                                      created,
                                      updated_on,
                                      tid=tid,
                                      tname=tname)
            return created_comment

    def remove(self, cid: str):
        sql = "DELETE FROM Comments WHERE id=:id"
        try:
            db.session.execute(sql, {"id": cid})
            db.session.commit()
        except Exception as error:
            raise DatabaseException('comment remove') from error


comment_repository = CommentRepository()
