from datetime import datetime
from entities.project import Project
from utils.database import db
from utils.exceptions import DatabaseException, NotExistingException
from entities.feature import Feature
from entities.task import Task
from utils.helpers import fullname


class FeatureRepository:
    """Class for handling Features in the database
    """

    def new(self, pid: str, pname: str, foid: str, foname: str, name: str, description: str, flags: str, status: str, ftype: str, priority: int) -> Feature:
        """new is used to create new features into the database

        Args:
            pid (str): id of associated project
            pname (str): name of associated project
            foid (str): id of associated feature owner
            foname (str): name of associated feature owner
            name (str): name of feature
            description (str): description of feature
            flags (str): flags used to identify features, given in string, example = "one;two;flags;"
            status (str): status of feature, for example "in progress", "waiting", "ready", "postponed"
            ftype (str): type of feature, for example "new feature", "bug fixes"
            priority (int): priority of feature, in three stages: low, severe and high (1 = low, 3 = high)

        Raises:
            DatabaseException: raised if problems occurs while saving into the database

        Returns:
            Feature: created feature as Feature object
        """
        values = {
            "project_id": pid,
            "feature_owner": foid,
            "name": name,
            "description": description,
            "flags": flags,
            "status": status,
            "type": ftype,
            "priority": priority
        }
        sql = """
        INSERT INTO Features
        (project_id, feature_owner, name, description, flags, status, type, priority)
        VALUES (:project_id, :feature_owner, :name, :description, :flags, :status, :type, :priority)
        RETURNING id, created, updated_on
        """

        try:
            fid, created, updated_on = db.session.execute(
                sql, values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException(
                'While saving new feature into database') from error

        if not fid:
            raise DatabaseException('While saving new feature into database')

        created_feature = Feature(fid, pid, pname, foid, foname, name, description,
                                  status, ftype, priority, created, updated_on, flags)

        return created_feature

    def get_all(self) -> [Feature]:
        """get_all is used to list of all projects in the database

        Raises:
            DatabaseException: raised if problems occur while interacting with the database

        Returns:
            [Feature]: list of all features as Feature object
        """
        sql = """
        SELECT F.id, F.project_id, P.name, F.feature_owner, U.firstname, U.lastname, F.name, F.description, F.flags, F.status, F.type, F.priority, F.created, F.updated_on  
        FROM Features F
        JOIN Projects P ON F.project_id = P.id
        JOIN Users U ON F.feature_owner = U.id
        """
        try:
            features = db.session.execute(sql).fetchall()
        except Exception as error:
            raise DatabaseException('while getting all features') from error

        all_tasks = None
        all_comments = None

        return [Feature(feature[0], feature[1], feature[2], feature[3], fullname(feature[4], feature[5]), feature[6], feature[7], feature[9], feature[10], feature[11], feature[12], feature[13], feature[8], all_tasks, all_comments) for feature in features]

    def get_all_by_project_id(self, pid: str) -> [Feature]:
        """get_all_by_project_id is used to get all features associated with given project

        Args:
            pid (str): id of project in which features must be associated

        Raises:
            DatabaseException: raised if problem occurs while interacting with the database

        Returns:
            [Feature]: list of found features
        """
        sql = """
        SELECT F.id, F.project_id, P.name, F.feature_owner, U.firstname, U.lastname, F.name, F.description, F.flags, F.status, F.type, F.priority, F.created, F.updated_on  
        FROM Features F
        JOIN Projects P ON F.project_id = P.id
        JOIN Users U ON F.feature_owner = U.id
        WHERE P.id=:id
        """
        try:
            features = db.session.execute(sql, {"id": pid}).fetchall()
        except Exception as error:
            raise DatabaseException(
                'while getting features with id') from error

        all_tasks = None
        all_comments = None

        return [Feature(feature[0], feature[1], feature[2], feature[3], fullname(feature[4], feature[5]), feature[6], feature[7], feature[9], feature[10], feature[11], feature[12], feature[13], feature[8], all_tasks, all_comments) for feature in features]

    def get_all_by_feature_owner(self, foid: str) -> [Feature]:
        """get_all_by_feature_owner is used get all features associated with given feature owner

        Args:
            foid (str): id of feature owner who owns found features

        Raises:
            DatabaseException: raised if problem occurs while interacting with the database

        Returns:
            [Feature]: list of found features
        """
        sql = """
        SELECT F.id, F.project_id, P.name, F.feature_owner, U.firstname, U.lastname, F.name, F.description, F.flags, F.status, F.type, F.priority, F.created, F.updated_on  
        FROM Features F
        JOIN Projects P ON F.project_id = P.id
        JOIN Users U ON F.feature_owner = U.id
        WHERE F.feature_owner=:id
        """
        try:
            features = db.session.execute(sql, {"id": foid}).fetchall()
        except Exception as error:
            raise DatabaseException(
                'while getting features with id') from error

        all_tasks = None
        all_comments = None

        return [Feature(feature[0], feature[1], feature[2], feature[3], fullname(feature[4], feature[5]), feature[6], feature[7], feature[9], feature[10], feature[11], feature[12], feature[13], feature[8], all_tasks, all_comments) for feature in features]

    def get_by_id(self, fid: str) -> Feature:
        """get_by_id is used to found feature with given id

        Args:
            fid (str): id of feature to be found

        Raises:
            DatabaseException: raised if problems while interacting with the database

        Returns:
            Feature: found feature
        """
        sql = """
        SELECT F.id, F.project_id, P.name, F.feature_owner, U.firstname, U.lastname, F.name, F.description, F.flags, F.status, F.type, F.priority, F.created, F.updated_on  
        FROM Features F
        JOIN Projects P ON F.project_id = P.id
        JOIN Users U ON F.feature_owner = U.id
        WHERE F.id=:id
        """
        try:
            feature = db.session.execute(sql, {"id": fid}).fetchone()
        except Exception as error:
            raise DatabaseException(
                'while getting features with id') from error

        all_tasks = None
        all_comments = None

        return Feature(feature[0], feature[1], feature[2], feature[3], fullname(feature[4], feature[5]), feature[6], feature[7], feature[9], feature[10], feature[11], feature[12], feature[13], feature[8], all_tasks, all_comments)

    def get_name(self, fid: str) -> str:
        """get_name is used to get name of feature with given id

        Args:
            fid (str): id of feature to be found

        Raises:
            DatabaseException: raised if problems while interacting with the database

        Returns:
            Feature: found feature
        """
        sql = """
        SELECT name
        FROM Features
        WHERE id=:id
        """
        try:
            name = db.session.execute(sql, {"id": fid}).fetchone()
        except Exception as error:
            raise DatabaseException(
                'while getting features with id') from error

        return name

    def update(self, fid: str, pid: str, pname: str, foid: str, foname: str, name: str, description: str, flags: str, status: str, ftype: str, priority: int) -> Feature:
        """update is used to update feature with given values into the database

        Args:
            fid (str): id of feature to be updated
            pid (str): id of associated project
            pname (str): name of associated project
            foid (str): id of associated feature owner
            foname (str): name of associated feature owner
            name (str): name of feature
            description (str): description of feature
            flags (str): flags used to identify features, given in string, example = "one;two;flags;"
            status (str): status of feature, for example "in progress", "waiting", "ready", "postponed"
            ftype (str): type of feature, for example "new feature", "bug fixes"
            priority (int): priority of feature, in three stages: low, severe and high (1 = low, 3 = high)

        Raises:
            DatabaseException: raised if problems occurs while saving into the database.

        Returns:
            Feature: updated feature object
        """
        values = {
            "project_id": pid,
            "feature_owner": foid,
            "name": name,
            "description": description,
            "flags": flags,
            "status": status,
            "type": ftype,
            "priority": priority
        }
        sql = """
        UPDATE Features
        SET project_id=:project_id, feature_owner=:feature_owner, name=:name, description=:description, flags=:flags, status=:status, type=:type, priority=:priority
        RETURNING created, updated_on
        """
        try:
            created, updated_on = db.session.execute(sql, values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException('feature update') from error

        all_tasks = None
        all_comments = None

        updated_feature = Feature(fid, pid, pname, foid, foname, name, description,
                                  status, ftype, priority, created, updated_on, flags, all_tasks, all_comments)
        return updated_feature

    def remove(self, fid: str) -> None:
        """remove is used to remove feature from the database

        Args:
            fid (str): id of feature which is removed

        Raises:
            DatabaseException: raised if problems occurs while interacting with database.
        """
        sql = "DELETE FROM Features WHERE id=:id"
        try:
            db.session.execute(sql, {"id": fid})
            db.session.commit()
        except Exception as error:
            raise DatabaseException('feature remove') from error


feature_repository = FeatureRepository()
