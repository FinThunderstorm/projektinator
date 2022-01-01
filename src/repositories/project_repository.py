from datetime import datetime

from entities.project import Project
from utils.database import db
from utils.exceptions import DatabaseException, NotExistingException
from entities.feature import Feature
from utils.helpers import fullname


class ProjectRepository:
    """Class used for handling projects in the database
    """

    def new(self, poid: str, poname: str, name: str, descrption: str,
            flags: str) -> Project:
        """new is used to create new projects into the database

        Args:
            poid (str): id of the project's owner
            poname (str): name of the project's owner
            name (str): name of the project
            descrption (str): description of the project
            flags (str): flags used to identify projects, given in string, example = "one;two;three;flags;"

        Raises:
            DatabaseException: raised DatabaseException if problems occurs while saving into the database

        Returns:
            Project: created project as Project objects
        """
        values = {
            "project_owner": poid,
            "name": name,
            "description": descrption,
            "flags": flags
        }

        sql = """
        INSERT INTO Projects
        (project_owner, name, description, flags)
        VALUES (:project_owner, :name, :description, :flags)
        RETURNING id, created, updated_on
        """

        try:
            pid, created, updated_on = db.session.execute(sql,
                                                          values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException(
                'While saving new project into database') from error
        if not pid:
            raise DatabaseException('While saving new project into database')
        created_project = Project(pid, poid, poname, name, descrption, created,
                                  updated_on, flags)

        return created_project

    def get_all(self) -> [Project]:
        """get_all is used to get list of all projects in the database

        Raises:
            DatabaseException: raised if problems occur while interacting with the database

        Returns:
            [Project]: list of all projects as project objects
        """
        sql = """
        SELECT P.id, P.project_owner, U.firstname, U.lastname, P.name, P.description, P.created, P.updated_on, P.flags 
        FROM Projects P 
        JOIN Users U ON P.project_owner = U.id
        """
        try:
            projects = db.session.execute(sql).fetchall()
        except Exception as error:
            raise DatabaseException('while getting all projects') from error
        all_features = None
        return [
            Project(project[0], project[1], fullname(project[2], project[3]),
                    project[4], project[5], project[6], project[7], project[8],
                    all_features) for project in projects
        ]

    def get_all_by_project_owner(self, poid: str) -> [Project]:
        """get_all_by_project_owner is used to get list of all projects associated with given project owner in the database

        Raises:
            DatabaseException: raised if problems occur while interacting with the database

        Returns:
            [Project]: list of all projects as project objects
        """
        sql = """
        SELECT P.id, P.project_owner, U.firstname, U.lastname, P.name, P.description, P.created, P.updated_on, P.flags 
        FROM Projects P 
        JOIN Users U ON P.project_owner = U.id
        WHERE P.project_owner=:id
        """
        try:
            projects = db.session.execute(sql, {"id": poid}).fetchall()
        except Exception as error:
            raise DatabaseException('while getting all projects') from error
        all_features = None
        return [
            Project(project[0], project[1], fullname(project[2], project[3]),
                    project[4], project[5], project[6], project[7], project[8],
                    all_features) for project in projects
        ]

    def get_by_id(self, pid: str) -> Project:
        """get_by_id is used to find exact project with given id from the database

        Args:
            pid (str): id of project to be found

        Raises:
            DatabaseException: raised if problems occur while interacting with the database
            NotExistingException: raised if there is none projects with given id

        Returns:
            Project: project with given id
        """
        sql = "SELECT P.id, P.project_owner, U.firstname, U.lastname, P.name, P.description, P.created, P.updated_on, P.flags FROM Projects P JOIN Users U ON P.project_owner = U.id WHERE P.id=:id"
        try:
            project = db.session.execute(sql, {"id": pid}).fetchone()
        except Exception as error:
            raise DatabaseException('while getting project by id') from error
        if not project:
            raise NotExistingException('Project')
        all_features = None
        return Project(project[0], project[1], fullname(project[2], project[3]),
                       project[4], project[5], project[6], project[7],
                       project[8], all_features)

    def get_name(self, pid: str) -> str:
        """get_name is used to find exact project with given id from the database

        Args:
            pid (str): id of project to be found

        Raises:
            DatabaseException: raised if problems occur while interacting with the database
            NotExistingException: raised if there is none projects with given id

        Returns:
            Project: project with given id
        """
        sql = "SELECT name FROM Projects WHERE id=:id"
        try:
            name = db.session.execute(sql, {"id": pid}).fetchone()
        except Exception as error:
            raise DatabaseException('while getting project by id') from error
        if not name:
            raise NotExistingException('Project')

        return name

    def update(self, pid: str, poid: str, poname: str, name: str,
               descrption: str, flags: str) -> Project:
        """update is used to update new values into database for specific Project.

        Args:
            pid (str): if of the project
            poid (str): id of the project's owner
            poname (str): name of the project's owner
            name (str): name of the project
            descrption (str): description of the project
            flags (str): flags used to identify projects, given in string, example = "one;two;three;flags;"
            features ([Feature]): list of Features that are linked to this Project.

        Raises:
            DatabaseException: raised if problem occurs while saving into the database.

        Returns:
            Project: updated Project object
        """
        values = {
            "id": pid,
            "project_owner": poid,
            "name": name,
            "description": descrption,
            "flags": flags
        }
        sql = "UPDATE Projects SET project_owner=:project_owner, name=:name, description=:description, flags=:flags WHERE id=:id RETURNING id, created, updated_on"
        try:
            project_id, created, updated_on = db.session.execute(
                sql, values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException(
                'While saving updated project into database') from error
        if str(pid) != str(project_id):
            raise DatabaseException(
                'While saving updated project into database')
        updated_project = Project(pid, poid, poname, name, descrption, created,
                                  updated_on, flags)
        return updated_project

    def remove(self, pid: str):
        """remove is used to remove project's from database

        Args:
            pid (str): id of project to be removed

        Raises:
            DatabaseException: raised if problems while interacting with database
        """

        sql = "DELETE FROM Projects WHERE id=:id"
        try:
            db.session.execute(sql, {"id": pid})
            db.session.commit()
        except Exception as error:
            raise DatabaseException('project remove') from error


project_repository = ProjectRepository()
