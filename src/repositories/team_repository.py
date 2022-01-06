from sqlalchemy.exc import IntegrityError
from utils.database import db
from utils.exceptions import DatabaseException, NotExistingException, UnvalidInputException
from entities.team import Team


class TeamRepository:
    '''Class for handling Teams in the database
    '''

    def new(self, name: str, description: str, tlid: str) -> str:
        '''new is used to create new teams into the database

        Args:
            name (str): name of the team
            description (str): description of the team
            tlid (str): id of the team leader

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database
            UnvalidInputException: raised if team leader
                is already in some team

        Returns:
            str: created team's id
        '''

        sql_teams = '''
            INSERT INTO Teams
            (name, description, team_leader)
            VALUES (:name, :description, :team_leader)
            RETURNING id
        '''

        sql_teamsusers = '''
            INSERT INTO Teamsusers
            (team_id, user_id)
            VALUES (:team_id, :user_id)
            RETURNING team_id, user_id
        '''

        values = {'name': name, 'description': description, 'team_leader': tlid}

        try:
            team_id = db.session.execute(sql_teams, values).fetchone()
            teid, user_id = db.session.execute(sql_teamsusers, {
                "team_id": team_id[0],
                "user_id": tlid
            })
            db.session.commit()
        except IntegrityError as error:
            raise UnvalidInputException(
                'Given team leader is already in some team',
                source='adding team leader to team') from error
        except Exception as error:
            raise DatabaseException('While saving new team') from error

        if not team_id:
            raise DatabaseException('While saving new team') from error

        if str(user_id) != str(tlid):
            raise DatabaseException('While saving new team')
        if str(team_id) != str(teid):
            raise DatabaseException('While saving new team')

        return team_id[0]

    def get_all(self) -> [tuple]:
        '''get_all is used to list of all teams in the database

        If no teams found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of all teams
        '''

        sql = '''
            SELECT T.id, T.name, T.description, T.team_leader, U.firstname, U.lastname
            FROM Teams T
            JOIN Users U ON T.team_leader = U.id
        '''

        try:
            teams = db.session.execute(sql).fetchall()
        except Exception as error:
            raise DatabaseException('While getting all teams') from error

        return [(team[0], team[1], team[2], team[3], team[4], team[5])
                for team in teams]

    def get_all_by_team_leader(self, tlid: str) -> [tuple]:
        '''get_all_by_team_leader is used get all teams
           associated with given team leader

        If no features found, returns empty list.

        Args:
            tlid (str): id of the team leader

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of found teams
        '''

        sql = '''
            SELECT T.id, T.name, T.description, T.team_leader, U.firstname, U.lastname
            FROM Teams T
            JOIN Users U ON T.team_leader = U.id
            WHERE T.team_leader=:id
        '''

        try:
            teams = db.session.execute(sql, {'id': tlid}).fetchall()
        except Exception as error:
            raise DatabaseException(
                'While getting all teams by team leader') from error

        return [(team[0], team[1], team[2], team[3], team[4], team[5])
                for team in teams]

    def get_by_id(self, teid: str) -> tuple:
        '''get_by_id is used to found team with given id

        Args:
            teid (str): id of the team

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if there is none teams with given id

        Returns:
            tuple: found team
        '''

        sql = '''
            SELECT T.id, T.name, T.description, T.team_leader, U.firstname, U.lastname
            FROM Teams T
            JOIN Users U ON T.team_leader = U.id
            WHERE T.id=:id
        '''

        try:
            team = db.session.execute(sql, {'id': teid}).fetchone()
        except Exception as error:
            raise DatabaseException('while getting team') from error

        if not team:
            raise NotExistingException('Team')

        return (team[0], team[1], team[2], team[3], team[4], team[5])

    def get_name(self, teid: str) -> str:
        '''get_name is used to get name of team with given id

        Args:
            teid (str): id of the team

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if team is not
                found with given id

        Returns:
            str: found name
        '''

        sql = '''
            SELECT name 
            FROM Teams T 
            WHERE id=:id
        '''

        try:
            name = db.session.execute(sql, {'id': teid}).fetchone()
        except Exception as error:
            raise DatabaseException("While getting team's name") from error

        return name[0]

    def update(self, teid: str, name: str, description: str, tlid: str) -> str:
        '''update is used to update team with given values into the database

        Args:
            teid (str): id of the team
            name (str): name of the team
            description (str): description of the team
            tlid (str): id of the team leader

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database
            UnvalidInputException: raised if team leader
                is already in some team

        Returns:
            str: updated team's id
        '''

        values = {
            'id': teid,
            'name': name,
            'description': description,
            'team_leader': tlid
        }

        sql = '''
            UPDATE Teams 
            SET name=:name, description=:description, team_leader=:team_leader
            WHERE id=:id 
            RETURNING id
        '''

        sql_teamsusers = '''
            INSERT INTO Teamsusers
            (team_id, user_id)
            VALUES (:team_id, :user_id)
            RETURNING team_id, user_id
        '''

        try:
            team_id = db.session.execute(sql, values).fetchone()
            teid_s, user_id = db.session.execute(sql_teamsusers, {
                "team_id": team_id[0],
                "user_id": tlid
            })
            db.session.commit()
        except IntegrityError as error:
            raise UnvalidInputException(
                'Given team leader is already in some team',
                source='adding team leader to team') from error
        except Exception as error:
            raise DatabaseException('While saving updated team') from error

        if str(teid) != str(team_id):
            raise DatabaseException('While saving updated team')

        if str(teid) != str(teid_s):
            raise DatabaseException("While saving updated team")

        return team_id[0]

    def add_member(self, teid: str, uid: str) -> tuple:
        '''add_member is used to add new members into team

        Args:
            teid (str): id of the team
            uid (str): id of the user

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            UnvalidInputException: raised if user
                is already in some team

        Returns:
            tuple: user and team ids
        '''

        sql = '''
            INSERT INTO Teamsusers
            (team_id, user_id)
            VALUES (:team_id, :user_id)
            RETURNING team_id, user_id
        '''

        values = {'team_id': teid, 'user_id': uid}

        try:
            team_id, user_id = db.session.execute(sql, values).fetchone()
            db.session.commit()
        except IntegrityError as error:
            raise UnvalidInputException('Given user is already in some team',
                                        source='adding user to team') from error
        except Exception as error:
            raise DatabaseException(
                'While saving new user into team') from error

        if str(teid) != str(team_id) or str(uid) != str(user_id):
            raise DatabaseException('While saving new user into team')

        return (team_id, user_id)

    def remove_member(self, teid: str, uid: str):
        '''remove_member is used to remove members from the team

        Args:
            teid (str): id of the team
            uid (str): id of the user

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
        '''

        sql = '''
            DELETE FROM Teamsusers
            WHERE (team_id=:team_id and user_id=:user_id)
        '''

        try:
            db.session.execute(sql, {'team_id': teid, 'user_id': uid})
            db.session.commit()
        except Exception as error:
            raise DatabaseException(
                'While removing members from team') from error

    def remove(self, teid: str):
        '''remove is used to remove feature from the database

        Args:
            fid (str): id of the feature to be removed

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
        '''

        sql = '''
            DELETE FROM Teams
            WHERE id=:id
        '''

        sql_tu = '''
            DELETE FROM Teamsusers
            WHERE team_id=:id
        '''

        try:
            db.session.execute(sql, {'id': teid})
            db.session.execute(sql_tu, {'id': teid})
            db.session.commit()
        except Exception as error:
            raise DatabaseException('team remove') from error


team_repository = TeamRepository()
