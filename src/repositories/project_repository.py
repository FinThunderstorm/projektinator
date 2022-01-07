from utils.database import db
from utils.exceptions import DatabaseException, NotExistingException


class ProjectRepository:
    '''Class used for handling projects in the database
    '''

    def new(self, poid: str, name: str, descrption: str, flags: str) -> tuple:
        '''new is used to create new projects into the database

        Args:
            poid (str): id of the project´s owner
            name (str): name of the project
            descrption (str): description of the project
            flags (str): flags used to identify projects,
                given in string, example = 'one;two;three;flags;'

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database

        Returns:
            tuple: created project´s id, creation and updated_on time
        '''

        values = {
            'project_owner': poid,
            'name': name,
            'description': descrption,
            'flags': flags
        }

        sql = '''
            INSERT INTO Projects
            (project_owner, name, description, flags)
            VALUES (:project_owner, :name, :description, :flags)
            RETURNING id, created, updated_on
        '''

        try:
            project_id, created, updated_on = db.session.execute(
                sql, values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException(
                'While saving new project into database') from error

        if not project_id:
            raise DatabaseException('While saving new project into database')

        return (project_id, created, updated_on)

    def get_all(self) -> [tuple]:
        '''get_all is used to get list of all projects in the database

        If no projects found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of all projects
        '''

        sql = '''
            SELECT P.id, P.project_owner, U.firstname, U.lastname, P.name, P.description, P.created, P.updated_on, P.flags 
            FROM Projects P 
            JOIN Users U ON P.project_owner = U.id
        '''

        try:
            projects = db.session.execute(sql).fetchall()
        except Exception as error:
            raise DatabaseException('While getting all projects') from error

        return [(project[0], project[1], project[2], project[3], project[4],
                 project[5], project[6], project[7], project[8])
                for project in projects]

    def get_projects(self) -> [tuple]:
        '''get_projects is used to get all projects for
           selecting projects in the frontend

        If no projects found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of project id and name
        '''

        sql = '''
            SELECT id, name
            FROM Projects
        '''

        try:
            projects = db.session.execute(sql).fetchall()
        except Exception as error:
            raise DatabaseException('While getting all projects') from error

        return [(project[0], project[1]) for project in projects]

    def get_all_by_project_owner(self, poid: str) -> [tuple]:
        '''get_all_by_project_owner is used get all projects
           associated with given project owner

        If no features found, returns empty list.

        Args:
            poid (str): id of the project´s owner

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of found projects
        '''

        sql = '''
            SELECT P.id, P.project_owner, U.firstname, U.lastname, P.name, P.description, P.created, P.updated_on, P.flags 
            FROM Projects P 
            JOIN Users U ON P.project_owner = U.id
            WHERE P.project_owner=:id
        '''

        try:
            projects = db.session.execute(sql, {'id': poid}).fetchall()
        except Exception as error:
            raise DatabaseException(
                'While getting all projects by Project Owner') from error

        return [(project[0], project[1], project[2], project[3], project[4],
                 project[5], project[6], project[7], project[8])
                for project in projects]

    def get_by_id(self, pid: str) -> tuple:
        '''get_by_id is used to find exact project with given id

        Args:
            pid (str): id of the project

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if there is none projects with given id

        Returns:
            tuple: found project
        '''

        sql = '''
            SELECT P.id, P.project_owner, U.firstname, U.lastname, P.name, P.description, P.created, P.updated_on, P.flags
            FROM Projects P 
            JOIN Users U ON P.project_owner = U.id 
            WHERE P.id=:id
        '''

        try:
            project = db.session.execute(sql, {'id': pid}).fetchone()
        except Exception as error:
            raise DatabaseException('While getting the project') from error

        if not project:
            raise NotExistingException('Project')

        return (project[0], project[1], project[2], project[3], project[4],
                project[5], project[6], project[7], project[8])

    def get_name(self, pid: str) -> str:
        '''get_name is used to get name of project with given id

        Args:
            pid (str): id of the project

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if project is not
                found with given id

        Returns:
            str: found name
        '''

        sql = '''
            SELECT name 
            FROM Projects 
            WHERE id=:id
        '''

        try:
            name = db.session.execute(sql, {'id': pid}).fetchone()
        except Exception as error:
            raise DatabaseException('While getting feature´s name') from error

        if not name:
            raise NotExistingException('Project')

        return name[0]

    def update(self, pid: str, poid: str, name: str, descrption: str,
               flags: str) -> tuple:
        '''update is used to update project with given values into the database

        Args:
            pid (str): if of the project
            poid (str): id of the project´s owner
            name (str): name of the project
            descrption (str): description of the project
            flags (str): flags used to identify projects,
                given in string, example = 'one;two;three;flags;'

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database

        Returns:
            tuple: updated project´s id, creation and updated on time
        '''

        values = {
            'id': pid,
            'project_owner': poid,
            'name': name,
            'description': descrption,
            'flags': flags
        }

        sql = '''
            UPDATE Projects 
            SET project_owner=:project_owner, name=:name, description=:description, flags=:flags 
            WHERE id=:id 
            RETURNING id, created, updated_on
        '''

        try:
            project_id, created, updated_on = db.session.execute(
                sql, values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException('While saving updated project') from error

        if str(pid) != str(project_id):
            raise DatabaseException('While saving updated project')

        return (project_id, created, updated_on)

    def remove(self, pid: str):
        '''remove is used to remove project from database

        Args:
            pid (str): id of the project to be removed

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
        '''

        sql = '''
            DELETE FROM Projects 
            WHERE id=:id
        '''

        try:
            db.session.execute(sql, {'id': pid})
            db.session.commit()
        except Exception as error:
            raise DatabaseException('While removing the project') from error


project_repository = ProjectRepository()
