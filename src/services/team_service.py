from entities.team import Team

from repositories.team_repository import TeamRepository, team_repository
from repositories.user_repository import UserRepository, user_repository

from utils.exceptions import NotExistingException, EmptyValueException, UnvalidInputException
from utils.helpers import fullname
from utils.validators import validate_uuid4


class TeamService:
    '''Class used for handling teams in the application'''

    def __init__(self,
                 default_team_repository: TeamRepository = team_repository,
                 default_user_repository: UserRepository = user_repository):
        '''Initializes TeamService

        Args:
            default_team_repository (TeamRepository, optional):
                interaction module with database for teams.
                Defaults to team_repository.
            default_user_repository (UserRepository, optional):
                interaction module with database for users.
                Defaults to user_repository.
        '''

        self._team_repository = default_team_repository
        self._user_repository = default_user_repository

    def new(self, name: str, description: str, tlid: str) -> Team:
        '''new is used to create new teams into the database

        Args:
            name (str): name of the team
            description (str): description of the team
            tlid (str): id of the team leader

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database
            EmptyValueException: raised if any given values is empty
            UnvalidInputException: raised if formatting of given
                input value is incorrect
            NotExistingException: raised if team leader
                with given id is not found

        Returns:
            Team: created team
        '''

        if (not name or not description or not tlid):
            raise EmptyValueException(
                'One of given values is empty, all values need to have value')

        if not validate_uuid4(tlid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='Team Leader ID')

        tlname = self._user_repository.get_fullname(tlid)

        if not tlname:
            raise NotExistingException('Team Leader')

        team_id = self._team_repository.new(name, description, tlid)

        created_team = Team(team_id, name, description, tlid, tlname)
        return created_team

    def get_all(self) -> [Team]:
        '''get_all is used to list of all teams in the database

        If no teams found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [Team]: list of all teams
        '''

        teams = [
            Team(team[0], team[1], team[2], team[3], fullname(team[4], team[5]))
            for team in self._team_repository.get_all()
        ]
        return teams

    def get_all_by_team_leader(self, tlid: str) -> [Team]:
        '''get_all_by_team_leader is used get all teams
           associated with given team leader

        If no features found, returns empty list.

        Args:
            tlid (str): id of the team leader

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if user with given
                id not found
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            [Team]: list of found teams
        '''

        if not validate_uuid4(tlid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='Team Leader ID')

        if not self._user_repository.get_by_id(tlid):
            raise NotExistingException('Team Leader')

        teams = teams = [
            Team(team[0], team[1], team[2], team[3], fullname(team[4], team[5]))
            for team in self._team_repository.get_all_by_team_leader(tlid)
        ]
        return teams

    def get_by_id(self, teid: str) -> Team:
        '''get_by_id is used to found team with given id

        Args:
            teid (str): id of the team

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if team is not
                found with given id
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            Team: found team
        '''

        if not validate_uuid4(teid):
            raise UnvalidInputException("team's id")

        team = self._team_repository.get_by_id(teid)
        return Team(team[0], team[1], team[2], team[3],
                    fullname(team[4], team[5]))

    def get_name(self, teid: str) -> str:
        '''get_name is used to get name of team with given id

        Args:
            teid (str): id of the team

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if team is not
                found with given id
            UnvalidInputException: raised if unvalid
                id is given

        Returns:
            str: found name
        '''

        if not validate_uuid4(teid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='team id')

        name = self._team_repository.get_name(teid)
        return name

    def update(self, teid: str, name: str, description: str, tlid: str) -> Team:
        '''update is used to update team with given values into the database

        Args:
            teid (str): id of the team
            name (str): name of the team
            description (str): description of the team
            tlid (str): id of the team leader

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database
            EmptyValueException: raised if any given values is empty
            UnvalidInputException: raised if formatting of given
                input value is incorrect
            NotExistingException: raised if team leader
                with given id is not found

        Returns:
            Team: updated team
        '''

        if (not teid or not name or not description or not tlid):
            raise EmptyValueException(
                'One of given values is empty, all values need to have value')

        if not validate_uuid4(teid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='Team ID')
        if not validate_uuid4(tlid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='Team Leader ID')

        tlname = self._user_repository.get_fullname(tlid)

        if not tlname:
            raise NotExistingException('Team Leader')

        team_id = self._team_repository.update(teid, name, description, tlid,
                                               tlname)

        updated_team = Team(team_id, name, description, tlid, tlname)
        return updated_team

    def add_member(self, teid: str, uid: str) -> tuple:
        '''add_member is used to add new members into team

        Args:
            teid (str): id of the team
            uid (str): id of the user

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            UnvalidInputException: raised if user
                is already in some team or given
                ids are incorrectly formatted
            NotExistingException: raised if team or user
                is not found with given id

        Returns:
            tuple: user and team ids
        '''

        if not validate_uuid4(teid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='Team ID')
        if not validate_uuid4(uid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='User ID')

        self._team_repository.get_by_id(teid)
        self._user_repository.get_by_id(uid)

        added = self._team_repository.add_member(teid, uid)
        return added

    def remove_member(self, teid: str, uid: str):
        '''remove_member is used to remove members from the team

        Args:
            teid (str): id of the team
            uid (str): id of the user

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            UnvalidInputException: raised if given
                ids are incorrectly formatted
            NotExistingException: raised if team or user
                is not found with given id
        '''

        if not validate_uuid4(teid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='Team ID')
        if not validate_uuid4(uid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='User ID')

        self._team_repository.get_by_id(teid)
        self._user_repository.get_by_id(uid)

        self._team_repository.remove_member(teid, uid)

    def remove(self, teid: str):
        '''remove is used to remove feature from the database

        Args:
            fid (str): id of the feature to be removed

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
        '''

        if not validate_uuid4(teid):
            raise UnvalidInputException(reason='unvalid formatting of uuid4',
                                        source='Team ID')

        self._team_repository.get_by_id(teid)
        self._team_repository.remove(teid)


team_service = TeamService()
