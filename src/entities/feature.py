from datetime import datetime
from entities.comment import Comment
from entities.task import Task


class Feature:
    """Class Feature resembles feature as a object from the database
    """

    def __init__(self, fid: str, pid: str, pname: str, foid: str, foname: str, name: str, description: str, status: str, feature_type: str, priority: int, created: datetime, updated_on: datetime, flags: str = "", tasks: [Task] = None, comments: [Comment] = None):
        """Initializes Feature object with given values

        Args:
            fid (str): id of feature
            pid (str): id of project in which references
            pname (str): name of project in which references
            name (str): name of feature
            description (str): description of feature
            status (str): status of feature
            feature_type (str): type of feature, like "new feature" or "bug fix"
            priority (int): priority of feature, in three stages: low, severe and high (1 = low, 3 = high)
            created (datetime): creation time of feature
            updated_on (datetime): latest time feature were updated on
            flags ([str], optional): flags are used to filter features. Defaults to None.
            tasks ([Task], optional): list of tasks referencing to feature. Defaults to None.
            comments ([Comment], optional): list of comments referencing to feature. Defaults to None.
        """
        self.feature_id = fid
        self.project_id = pid
        self.project_name = pname
        self.feature_owner = foid
        self.feature_owner_name = foname
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

    def __str__(self) -> str:
        """Method for generating formatted string from object to be mainly used in debugging matters.

        Returns:
            str: feature object in formatted string
        """
        comments = ""
        if self.comments:
            for comment in self.comments:
                comments += f'   › {comment.comment_id}\n'
        tasks = ""
        if self.tasks:
            for task in self.tasks:
                tasks += f'   › {task.name} ({task.task_id})\n'
        return (
            f'Feature ”{self.name}”: \n'
            f' - id ”{self.feature_id}”\n'
            f' - is related to project ”{self.project_name} ({self.project_id})”\n'
            f' - description ”{self.description}”\n'
            f' - status ”{self.status}”\n'
            f" - feature's type ”{self.feature_type}”\n"
            f' - priority ”{self.priority}”\n'
            f' - created on ”{self.created}”\n'
            f' - updated on ”{self.updated_on}”\n'
            f' - flags ”{self.flags}”\n'
            f' - tasks:\n{tasks}'
            f' - comments:\n{comments}'
        )
