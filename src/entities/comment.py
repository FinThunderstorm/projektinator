from datetime import datetime


class Comment:
    """Class Comment resembles comment and activity in features or in tasks.
    """

    def __init__(self, cid: str, aid: str, comment: str, added_on: datetime, tid: str = None, fid: str = None):
        """Initializes Comment with given values

        Args:
            cid (str): id of comment, uuid4 formatted by database
            aid (str): id of comment's assignee
            comment (str): description of what have been done
            added_on (datetime): datetime when added into database
            tid (str, optional): id of task into which references. Defaults to None.
            fid (str, optional): id of feature into which references. Defaults to None.
        """
        self.comment_id = cid
        self.task_id = tid
        self.feature_id = fid
        self.assignee_id = aid
        self.comment = comment
        self.added_on = added_on
