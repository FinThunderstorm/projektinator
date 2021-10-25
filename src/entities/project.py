from datetime import datetime
from entities.feature import Feature


class Project:
    """Class Project resembles project from the database as a object
    """

    def __init__(self, pid: str, p_owner: str, p_owner_name: str, name: str, description: str, created: datetime, flags: [str] = None, features: [Feature] = None):
        """[summary]

        Args:
            pid (str): id of project
            p_owner (str): id of project owner
            p_owner_name (str): name of project owner
            name (str): name of project
            description (str): description of project
            created (datetime): creation time of project
            flags ([str], optional): flags are used to filter projects. Defaults to None.
            features ([Feature], optional): list of features referencing to project. Defaults to None.
        """
        self.project_id = pid
        self.project_owner_id = p_owner
        self.project_owner_name = p_owner_name
        self.name = name
        self.description = description
        self.created = created
        self.flags = flags
        self.features = features