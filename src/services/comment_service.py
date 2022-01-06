from entities.comment import Comment
from repositories.comment_repository import comment_repository, CommentRepository
from repositories.feature_repository import feature_repository, FeatureRepository
from repositories.user_repository import user_repository, UserRepository
from repositories.task_repository import task_repository, TaskRepository
from utils.exceptions import EmptyValueException, UnvalidInputException, NotExistingException
from utils.validators import validate_uuid4
from utils.helpers import fullname


class CommentService:
    """Class used for handling comments in the application
    """

    def __init__(
        self,
        default_comment_repository: CommentRepository = comment_repository,
        default_feature_repository: FeatureRepository = feature_repository,
        default_task_repository: TaskRepository = task_repository,
        default_user_repository: UserRepository = user_repository,
    ):
        """Initializes CommentService

        Args:
            default_comment_repository (CommentRepository, optional):
                interaction module with database for comments.
                Defaults to comment_repository.
            default_feature_repository (FeatureRepository, optional):
                interaction module with database for features.
                Defaults to feature_repository.
            default_task_repository (TaskRepository, optional):
                interaction module with database for tasks.
                Defaults to task_repository.
            default_user_repository (UserRepository, optional):
                interaction module with database for users.
                Defaults to user_repository.
        """

        self._comment_repository = default_comment_repository
        self._feature_repository = default_feature_repository
        self._task_repository = default_task_repository
        self._user_repository = default_user_repository

    def new(self,
            aid: str,
            comment: str,
            tspent: str = "0.0",
            tid: str = None,
            fid: str = None) -> Comment:
        """new is used to create new comments

        Args:
            aid (str): id of the comments's assignee
            comment (str): content of the comment
            tspent (float): time spent, used for time tracking
            tid (str, optional): id of the related task. Defaults to None.
            fid (str, optional): id of the related feature. Defaults to None.

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database
            NotExistingException: raised if given assignee, feature
                or task is not found
            UnvalidInputException: raised if unvalid time spent given,
                or unvalid id is given
            EmptyValueException: raised if any given values is empty

        Returns:
            Comment: created comment
        """

        if not aid or not comment or not tspent:
            raise EmptyValueException(
                "One of given values is empty, all values need to have value")

        if not validate_uuid4(aid):
            raise UnvalidInputException("comment's assignee id")

        aname = self._user_repository.get_fullname(aid)
        if not aname:
            raise NotExistingException("comment's assignee")

        try:
            tspent = float(tspent)
        except ValueError as error:
            raise UnvalidInputException(
                source="comment's time spent") from error
        except TypeError as error:
            raise UnvalidInputException(
                source="comment's time spent") from error

        if fid:
            if not validate_uuid4(fid):
                raise UnvalidInputException("comment's feature id")

            fname = self._feature_repository.get_name(fid)

            if not fname:
                raise NotExistingException("comment's related feature")

            comment_id, created, updated_on = self._comment_repository.new(
                aid,
                comment,
                tspent,
                fid=fid,
            )
            created_comment = Comment(comment_id,
                                      aid,
                                      aname,
                                      tspent,
                                      comment,
                                      created,
                                      updated_on,
                                      fid=fid,
                                      fname=fname)
        elif tid:
            if not validate_uuid4(tid):
                raise UnvalidInputException("comment's task id")

            tname = self._task_repository.get_name(tid)

            if not tname:
                raise NotExistingException("comment's related task")

            comment_id, created, updated_on = self._comment_repository.new(
                aid,
                comment,
                tspent,
                tid=tid,
            )
            created_comment = Comment(comment_id,
                                      aid,
                                      aname,
                                      tspent,
                                      comment,
                                      created,
                                      updated_on,
                                      tid=tid,
                                      tname=tname)
        else:
            raise EmptyValueException(
                "Adding comment", "either feature or task id needs to be given")
        return created_comment

    def get_all_by_feature_id(self, fid: str) -> [Comment]:
        """get_all_by_feature_id is used to get list of all comments
           associated with given feature id in the database.

           If no comments found, returns empty list.

        Args:
            fid (str): id of the related feature

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            [Comment]: list of found comments
        """
        if not validate_uuid4(fid):
            raise UnvalidInputException("comment's feature id")

        comments = [
            Comment(comment[1],
                    comment[2],
                    fullname(comment[3], comment[4]),
                    comment[5],
                    comment[6],
                    comment[7],
                    comment[8],
                    fid=comment[9],
                    fname=comment[10],
                    mode=comment[0])
            for comment in self._comment_repository.get_all_by_feature_id(fid)
        ]

        return comments

    def get_all_by_task_id(self, tid: str) -> [Comment]:
        """get_all_by_task_id is used to get list of all comments
           associated with given task id in the database.

           If no comments found, returns empty list.

        Args:
            tid (str): id of the related task

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            [Comment]: list of found comments
        """
        if not validate_uuid4(tid):
            raise UnvalidInputException("comment's task id")

        comments = comments = [
            Comment(comment[1],
                    comment[2],
                    fullname(comment[3], comment[4]),
                    comment[5],
                    comment[6],
                    comment[7],
                    comment[8],
                    tid=comment[9],
                    tname=comment[10],
                    mode=comment[0])
            for comment in self._comment_repository.get_all_by_task_id(tid)
        ]
        return comments

    def get_all_by_assignee(self, aid: str) -> [Comment]:
        """get_all_by_assignee is used to get list of all comments
           associated with given assignee's id in the database.

           If no comments found, returns empty list.

        Args:
            aid (str): id of the related assignee

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            [Comment]: list of found comments
        """
        if not validate_uuid4(aid):
            raise UnvalidInputException("comment's assignee id")

        comments = self._comment_repository.get_all_by_assignee(aid)
        comments = [
            Comment(comment[1],
                    comment[2],
                    fullname(comment[3], comment[4]),
                    comment[5],
                    comment[6],
                    comment[7],
                    comment[8],
                    fid=comment[9],
                    fname=comment[10],
                    mode=comment[0]) if comment[0] == "features" else Comment(
                        comment[1],
                        comment[2],
                        fullname(comment[3], comment[4]),
                        comment[5],
                        comment[6],
                        comment[7],
                        comment[8],
                        tid=comment[9],
                        tname=comment[10],
                        mode=comment[0])
            for comment in self._comment_repository.get_all_by_assignee(aid)
        ]

        return comments

    def get_by_id(self, cid: str) -> Comment:
        """get_by_id is used to find exact comment with
           given id from the database

        Args:
            cid (str): id of the comment to be found

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            UnvalidInputException: raised if unvalid
                id is given
            NotExistingException: raised if there is none
                comments with given id

        Returns:
            Comment: comment with given id
        """
        if not validate_uuid4(cid):
            raise UnvalidInputException("comment's id")

        comment = self._comment_repository.get_by_id(cid)

        if not comment:
            raise NotExistingException("Comment")

        if comment[0] == "features":
            return Comment(comment[1],
                           comment[2],
                           fullname(comment[3], comment[4]),
                           comment[5],
                           comment[6],
                           comment[7],
                           comment[8],
                           fid=comment[9],
                           fname=comment[10])
        else:
            return Comment(comment[1],
                           comment[2],
                           fullname(comment[3], comment[4]),
                           comment[5],
                           comment[6],
                           comment[7],
                           comment[8],
                           tid=comment[9],
                           tname=comment[10])

    def update(self,
               cid: str,
               aid: str,
               comment_text: str,
               tspent: str,
               tid: str = None,
               fid: str = None) -> Comment:
        """update is used to update new values into
           the database for specific comment

        Args:
            cid (str): id of the comment
            aid (str): id of the comments's assignee
            comment_text (str): content of the comment
            tspent (float): time spent, used for time tracking
            tid (str, optional): id of the related task. Defaults to None.
            fid (str, optional): id of the related feature. Defaults to None.

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database
            NotExistingException: raised if given comment, assignee,
                feature or task is not found
            UnvalidInputException: raised if unvalid time spent given,
                or unvalid id is given
            EmptyValueException: raised if any given values is empty

        Returns:
            Comment: updated comment
        """
        if not cid or not aid or not comment_text or not tspent:
            raise EmptyValueException(
                "One of given values is empty, all values need to have value")

        if not validate_uuid4(cid):
            raise UnvalidInputException("comment's id")

        if not validate_uuid4(aid):
            raise UnvalidInputException("comment's assignee id")

        comment = self.get_by_id(cid)
        aname = self._user_repository.get_fullname(aid)

        if not aname:
            raise NotExistingException("comment's assignee")

        try:
            tspent = float(tspent)
        except ValueError as error:
            raise UnvalidInputException(
                source="comment's time spent") from error
        except TypeError as error:
            raise UnvalidInputException(
                source="comment's time spent") from error

        if fid:
            if not validate_uuid4(fid):
                raise UnvalidInputException("comment's feature id")

            fname = self._feature_repository.get_name(fid)

            if not fname:
                raise NotExistingException("comment's related feature")

            comment_id, created, updated_on = self._comment_repository.update(
                comment.comment_id, aid, comment_text, fid=fid)
            updated_comment = Comment(comment_id,
                                      aid,
                                      aname,
                                      tspent,
                                      comment,
                                      created,
                                      updated_on,
                                      fid=fid,
                                      fname=fname)
        elif tid:
            if not validate_uuid4(tid):
                raise UnvalidInputException("comment's task id")
            tname = self._task_repository.get_name(tid)

            if not tname:
                raise NotExistingException("comment's related task")

            comment_id, created, updated_on = self._comment_repository.update(
                comment.comment_id, aid, comment_text, tspent, tid=tid)
            updated_comment = Comment(comment_id,
                                      aid,
                                      aname,
                                      tspent,
                                      comment,
                                      created,
                                      updated_on,
                                      tid=tid,
                                      tname=tname)
        else:
            raise EmptyValueException(
                "Updating comment",
                "either feature or task id needs to be given")

        return updated_comment

    def remove(self, cid: str):
        """remove is used to remove comment from the database

        Args:
            cid (str): id of comment to be removed

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            UnvalidInputException: raised if unvalid
                id is given
            NotExistingException: raised if there is none
                comments with given id
        """

        if not validate_uuid4(cid):
            raise UnvalidInputException(reason="unvalid formatting of uuid4",
                                        source="comment id")

        self._comment_repository.get_by_id(cid)
        self._comment_repository.remove(cid)


comment_service = CommentService()
