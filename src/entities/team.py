from entities.user import User


class Team:
    """Class Team resembles user as a object from the database.
    """

    def __init__(self,
                 teid: str,
                 name: str,
                 description: str,
                 tlid: str,
                 tlname: str,
                 members: [User] = None):
        self.team_id = teid
        self.name = name
        self.description = description
        self.team_leader_id = tlid
        self.team_leader_name = tlname
        self.members = members

    def __str__(self) -> str:
        """Method for generating formatted string from object to be mainly used in debugging matters.

        Returns:
            str: team object in formatted string
        """
        members = ""
        if self.members:
            for member in self.members:
                members += f'   › {member.fullname} ({member.user_id})\n'

        return (
            f'Team ”{self.name} ({self.team_id})”\n'
            f" - description ”{self.description}”\n"
            f' - team leader ”{self.team_leader_name} ({self.team_leader_name})”\n'
            f' - members\n”{members}”')
