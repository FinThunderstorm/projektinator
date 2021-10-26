from datetime import datetime
from entities.feature import Feature


class Project:
    """Class Project resembles project from the database as a object
    """

    def __init__(self, pid: str, p_owner: str, p_owner_name: str, name: str, description: str, created: datetime, updated_on: datetime, flags: str = "", features: [Feature] = None):
        """initializes Project object

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
        self.updated_on = updated_on
        self.flags = flags
        self.features = features

    def __str__(self) -> str:
        """Method for generating formatted string from object to be mainly used in debugging matters.

        Returns:
            str: project object in formatted string
        """
        features = ""
        if self.features:
            for feature in self.features:
                features += f'   › {feature.name} ({feature.feature_id})\n'
        return (
            f'Project ”{self.name}”: \n'
            f' - id ”{self.project_id}”\n'
            f' - product owner ”{self.project_owner_name} ({self.project_owner_id})”\n'
            f' - description ”{self.description}”\n'
            f' - created ”{self.created}”\n'
            f' - updated on ”{self.updated_on}”\n'
            f' - flags ”{self.flags}”\n'
            f' - features:\n{features}'
        )
