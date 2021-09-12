from datetime import datetime
from entities.comment import Comment


class Task:
    """Class Task resembles tasks as a object from the database.
    """

    def __init__(self, tid: str, fid: str, aid: str, assignee_name: str, name: str, description: str, status: str, task_type: str, priority: int, created: datetime, updated_on: datetime, flags: [str] = None, comments: [Comment] = None):
        """Initializes Task object with given values

        Args:
            tid (str): id of task
            fid (str): id of feature in which references
            aid (str): id of assignee
            assignee_name (str): name of assignee
            name (str): name of task
            description (str): description of task
            status (str): status of task
            task_type (str): type of task, like "new feature" or "bug fix"
            priority (int): priority in three stages: low, severate and high
            created (datetime): creation time of task
            updated_on (datetime): latest time task is updated on
            flags ([str], optional): flags are used to filter tasks. Defaults to None.
            comments ([Comment], optional): list of activity related to comment. Defaults to None.
        """
        self.task_id = tid
        self.feature_id = fid
        self.assignee_id = aid
        self.assignee_name = assignee_name
        self.name = name
        self.description = description
        self.status = status
        self.task_type = task_type
        self.priority = priority
        self.created = created
        self.updated_on = updated_on
        self.flags = flags
        self.comments = comments
