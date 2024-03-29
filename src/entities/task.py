from datetime import datetime
from entities.comment import Comment


class Task:
    '''Class Task resembles tasks as a object from the database.
    '''

    def __init__(self,
                 tid: str,
                 fid: str,
                 fname: str,
                 assignee: str,
                 assignee_name: str,
                 name: str,
                 description: str,
                 status: str,
                 status_name: str,
                 task_type: str,
                 task_type_name: str,
                 priority: int,
                 created: datetime,
                 updated_on: datetime,
                 flags: str = '',
                 comments: [Comment] = None):
        '''Initializes Task object with given values

        Args:
            tid (str): id of task
            fid (str): id of feature in which references
            fname (str): name of the feature
            assignee (str): id of assignee
            assignee_name (str): name of assignee
            name (str): name of task
            description (str): description of task
            status (str): status of task
            status_name (str): name of the status
            task_type (str): type of task, like 'new feature' or 'bug fix'
            task_type_name (str): name of the task type
            priority (int): priority in three stages: low, severate and high
            created (datetime): creation time of task
            updated_on (datetime): latest time task is updated on
            flags (str, optional): flags are used to filter tasks.
                Defaults to None.
            comments ([Comment], optional): list of activity related to comment.
                Defaults to None.
        '''

        self.task_id = tid
        self.feature_id = fid
        self.feature_name = fname
        self.assignee_id = assignee
        self.assignee_name = assignee_name
        self.name = name
        self.description = description
        self.status = status
        self.status_name = status_name
        self.task_type = task_type
        self.task_type_name = task_type_name
        self.priority = priority
        self.created = created
        self.updated_on = updated_on
        self.flags = flags
        self.comments = comments

    def __str__(self) -> str:
        '''Method for generating formatted string from object
           to be mainly used in debugging matters.

        Returns:
            str: task object in formatted string
        '''

        comments = ''
        if self.comments:
            for comment in self.comments:
                comments += f'   › {comment.comment_id}\n'

        fid = self.feature_id
        fname = self.feature_name

        return (f'Task ”{self.name}”: \n'
                f' - id ”{self.task_id}”\n'
                f' - is related to feature ”{fname} ({fid})”\n'
                f' - assignee ”{self.assignee_name} ({self.assignee_id})”\n'
                f' - description ”{self.description}”\n'
                f' - status ”{self.status_name}”\n'
                f' - tasks type ”{self.task_type_name}”\n'
                f' - priority ”{self.priority}”\n'
                f' - created on ”{self.created}”\n'
                f' - updated on ”{self.updated_on}”\n'
                f' - flags ”{self.flags}”\n'
                f' - comments\n”{comments}”')
