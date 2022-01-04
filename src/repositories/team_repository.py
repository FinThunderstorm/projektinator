from utils.database import db
from utils.exceptions import DatabaseException, NotExistingException
from entities.team import Team
from repositories.user_repository import user_repository
from utils.helpers import fullname


class TeamRepository:

    def new(self, name: str, description: str, tlid: str, tlname: str):
        sql = """
        INSERT INTO Teams
        (name, description, team_leader)
        VALUES (:name, :description, :team_leader)
        RETURNING id
        """

        values = {"name": name, "description": description, "team_leader": tlid}

        try:
            teid = db.session.execute(sql, values).fetchone()[0]
            db.session.commit()
        except Exception as error:
            raise DatabaseException(
                'While saving new team into database') from error

        if not teid:
            raise DatabaseException(
                'While saving new team into database') from error

        new_team = Team(teid, name, description, tlid, tlname)

        return new_team

    def get_all(self):
        sql = """
            SELECT T.id, T.name, T.description, T.team_leader, U.firstname, U.lastname
            FROM Teams T
            JOIN Users U ON T.team_leader = U.id
        """
        try:
            teams = db.session.execute(sql).fetchall()
        except Exception as error:
            raise DatabaseException('while getting all teams') from error

        return [
            Team(team[0], team[1], team[2], team[3], fullname(team[4], team[5]),
                 user_repository.get_by_team(team[0])) for team in teams
        ]

    def get_by_team_leader(self, tlid: str):
        sql = """
            SELECT T.id, T.name, T.description, T.team_leader, U.firstname, U.lastname
            FROM Teams T
            JOIN Users U ON T.team_leader = U.id
            WHERE T.team_leader=:id
        """
        try:
            teams = db.session.execute(sql, {"id": tlid}).fetchall()
        except Exception as error:
            raise DatabaseException('while getting all teams') from error

        return [
            Team(team[0], team[1], team[2], team[3], fullname(team[4], team[5]),
                 user_repository.get_by_team(team[0])) for team in teams
        ]

    def get_by_id(self, teid: str):
        sql = """
            SELECT T.id, T.name, T.description, T.team_leader, U.firstname, U.lastname
            FROM Teams T
            JOIN Users U ON T.team_leader = U.id
            WHERE T.id=:id
        """
        try:
            team = db.session.execute(sql, {"id": teid}).fetchone()
        except Exception as error:
            raise DatabaseException('while getting team') from error

        return Team(team[0], team[1], team[2], team[3],
                    fullname(team[4], team[5]),
                    user_repository.get_by_team(team[0]))

    def get_name(self, teid: str):
        sql = """
            SELECT name 
            FROM Teams T 
            WHERE id=:id
        """
        try:
            team = db.session.execute(sql, {"id": teid}).fetchone()
        except Exception as error:
            raise DatabaseException('while getting name for team') from error

        return team

    def update(self, teid: str, name: str, description: str, tlid: str,
               tlname: str):
        values = {
            "id": teid,
            "name": name,
            "description": description,
            "team_leader": tlid
        }
        sql = """
            UPDATE Teams 
            SET name=:name, description=:description, team_leader=:team_leader
            WHERE id=:id 
            RETURNING id
        """
        try:
            team_id = db.session.execute(sql, values).fetchone()[0]
            db.session.commit()
        except Exception as error:
            print(error)
            raise DatabaseException(
                'While saving updated team into database') from error
        if str(teid) != str(team_id):
            print('h')
            raise DatabaseException('While saving updated team into database')

        return Team(teid, name, description, tlid, tlname,
                    user_repository.get_by_team(teid))

    def add_member(self, teid: str, uid: str):
        sql = """
            INSERT INTO Teamsusers
            (team_id, user_id)
            VALUES (:team_id, :user_id)
            RETURNING team_id, user_id
        """
        values = {"team_id": teid, "user_id": uid}
        try:
            team_id, user_id = db.session.execute(sql, values).fetchone()
            db.session.commit()
        except Exception as error:
            print(error)
            raise DatabaseException(
                'While saving new user into team') from error

        if str(teid) != str(team_id) or str(uid) != str(user_id):
            print('hh')
            raise DatabaseException('While saving new user into team')

        return (team_id, user_id)

    def remove_member(self, teid: str, uid: str):
        sql = """
            DELETE FROM Teamsusers
            WHERE (team_id=:team_id and user_id=:user_id)
        """
        try:
            db.session.execute(sql, {"team_id": teid, "user_id": uid})
            db.session.commit()
        except Exception as error:
            raise DatabaseException('team member remove') from error

    def remove(self, teid: str):
        sql = """
            DELETE FROM Teams
            WHERE id=:id
        """
        sql_tu = """
            DELETE FROM Teamsusers
            WHERE team_id=:id
        """
        try:
            db.session.execute(sql, {"id": teid})
            db.session.execute(sql_tu, {"id": teid})
            db.session.commit()
        except Exception as error:
            raise DatabaseException('team remove') from error


team_repository = TeamRepository()
