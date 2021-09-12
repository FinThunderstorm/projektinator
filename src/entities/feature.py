from datetime import datetime
from entities.comment import Comment
from entities.task import Task


class Feature:
    """Class Feature resembles feature as a object from the database
    """

    def __init__(self, fid: str, pid: str, name: str, description: str, status: str, feature_type: str, priority: int, created: datetime, updated_on: datetime, flags: [str] = None, tasks: [Task] = None, comments: [Comment] = None):
        """Initializes Feature object with given values

        Args:
            fid (str): id of feature
            pid (str): id of project in which references
            name (str): name of feature
            description (str): description of feature
            status (str): status of feature
            feature_type (str): type of feature, like "new feature" or "bug fix"
            priority (int): priority of feature, in three stages: low, severe and high
            created (datetime): creation time of feature
            updated_on (datetime): latest time feature were updated on
            flags ([str], optional): flags are used to filter features. Defaults to None.
            tasks ([Task], optional): list of tasks referencing to feature. Defaults to None.
            comments ([Comment], optional): list of comments referencing to feature. Defaults to None.
        """
        self.feature_id = fid
        self.project_id = pid
        self.name = name
        self.description = description
        self.status = status
        self.feature_type = feature_type
        self.priority = priority
        self.created = created
        self.updated_on = updated_on
        self.flags = flags
        self.tasks = tasks
        self.comments = comments
