from utils.exceptions import DatabaseException, NotExistingException
from repositories.team_repository import TeamRepository, team_repository
from repositories.user_repository import UserRepository, user_repository
from utils.helpers import fullname


class TeamService:

    def __init__(self,
                 default_team_repository: TeamRepository = team_repository,
                 default_user_repository: UserRepository = user_repository):
        self._team_repository = default_team_repository
        self._user_repository = default_user_repository

    def new(self, name: str, description: str, tlid: str):
        tlname = self._user_repository.get_fullname(tlid)
        new_team = self._team_repository.new(name, description, tlid, tlname)
        return new_team

    def get_all(self):
        teams = self._team_repository.get_all()
        return teams

    def get_by_id(self, teid: str):
        team = self._team_repository.get_by_id(teid)
        return team

    def get_name(self, teid: str):
        name = self._team_repository.get_name(teid)
        return name

    def update(self, teid: str, name: str, description: str, tlid: str):
        tlname = self._user_repository.get_fullname(tlid)
        updated_team = self._team_repository.update(teid, name, description,
                                                    tlid, tlname)
        return updated_team

    def add_member(self, teid: str, uid: str):
        added = self._team_repository.add_member(teid, uid)
        return added

    def remove_member(self, teid: str, uid: str):
        self._team_repository.remove_member(teid, uid)

    def remove(self, teid: str):
        self._team_repository.remove(teid)


team_service = TeamService()
