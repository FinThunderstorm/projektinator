from datetime import datetime


class Comment:
    """Class Comment resembles comment and activity in features or in tasks.
    """

    def __init__(self, cid: str, aid: str, aname: str, comment: str, added_on: datetime, tid: str = None, tname: str = None, fid: str = None, fname: str = None):
        """Initializes Comment with given values. Is optional to use with tasks or features.

        Args:
            cid (str): id of comment, uuid4 formatted by database
            aid (str): id of comment's assignee
            aname(str): name of comment's assignee
            comment (str): description of what have been done
            added_on (datetime): datetime when added into database
            tid (str, optional): id of task into which references. Defaults to None.
            tname (str, optional): name of task into which references. Defaults to None.
            fid (str, optional): id of feature into which references. Defaults to None.
            tname (str, optional): name of task into which references. Defaults to None.
        """
        self.comment_id = cid
        self.task_id = tid
        self.task_name = tname
        self.feature_id = fid
        self.feature_name = fname
        self.assignee_id = aid
        self.assignee_name = aname
        self.comment = comment
        self.added_on = added_on

    def __str__(self) -> str:
        """Method for generating formatted string from object to be mainly used in debugging matters.

        Returns:
            str: comment object in formatted string
        """
        relates = f"task ”{self.task_name} ({self.task_name})”" if self.task_id else f"feature ”{self.feature_name} ({self.feature_id})”"
        return (
            f'Comment ”{self.comment_id}”: \n'
            f' - is related to {relates}\n'
            f' - assignee ”{self.assignee_name} ({self.assignee_id})”\n'
            f' - comment ”{self.comment}”\n'
            f' - added on ”{self.added_on}”'
        )
