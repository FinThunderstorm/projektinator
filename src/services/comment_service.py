from datetime import datetime
from entities.comment import Comment
from repositories.comment_repository import comment_repository, CommentRepository
from repositories.feature_repository import feature_repository, FeatureRepository
from repositories.user_repository import user_repository, UserRepository
from repositories.task_repository import task_repository, TaskRepository
from utils.exceptions import EmptyValueException, UnvalidInputException, NotExistingException
from utils.validators import validate_flags, validate_uuid4


class CommentService:
    """Class used for handling comments in the application
    """

    def __init__(
        self,
        default_comment_repository: CommentRepository = comment_repository,
        default_feature_repository: FeatureRepository = feature_repository,
        default_user_repository: UserRepository = user_repository,
        default_task_repository: TaskRepository = task_repository,
    ):
        """Initializes Comments Service

        Args:
            default_comment_repository (CommentRepository, optional): interaction module with database for comments. Defaults to comment_repository.
        """
        self._comment_repository = default_comment_repository
        self._feature_repository = default_feature_repository
        self._user_repository = default_user_repository
        self._task_repository = default_task_repository

    def new(self,
            aid: str,
            comment: str,
            tspent: str = "0.0",
            tid: str = None,
            fid: str = None):
        aname = self._user_repository.get_fullname(aid)

        try:
            tspent = float(tspent)
        except Exception as error:
            raise UnvalidInputException()

        if fid != None:
            fname = self._feature_repository.get_name(fid)
            created_comment = self._comment_repository.new(aid,
                                                           aname,
                                                           comment,
                                                           tspent,
                                                           fid=fid,
                                                           fname=fname)
        else:
            tname = self._task_repository.get_name(tid)
            created_comment = self._comment_repository.new(aid,
                                                           aname,
                                                           comment,
                                                           tspent,
                                                           tid=tid,
                                                           tname=tname)
        return created_comment

    def get_by_feature_id(self, fid: str):
        comments = self._comment_repository.get_by_feature_id(fid)
        if comments is None:
            comments = []
        return comments

    def get_by_task_id(self, tid: str):
        comments = self._comment_repository.get_by_task_id(tid)
        if comments is None:
            comments = []
        return comments

    def get_by_assignee(self, aid: str):
        comments = self._comment_repository.get_by_assignee(aid)
        if comments is None:
            comments = []
        return comments

    def get_by_id(self, cid: str):
        comment = self._comment_repository.get_by_id(cid)
        return comment

    def update(self,
               cid: str,
               aid: str,
               comment_text: str,
               tspent: float,
               tid: str = None,
               fid: str = None):
        comment = self.get_by_id(cid)
        aname = self._user_repository.get_fullname(aid)
        tname = self._task_repository.get_name(tid)
        fname = self._feature_repository.get_name(fid)

        updated_comment = self._comment_repository.update(
            cid, aid, aname, comment_text, tspent, tid, tname, fid, fname)

        return updated_comment

    def remove(self, cid: str):
        self._comment_repository.remove(cid)


comment_service = CommentService()
