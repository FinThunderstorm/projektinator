from utils.database import db
from utils.exceptions import DatabaseException, NotExistingException


class FeatureRepository:
    '''Class for handling Features in the database
    '''

    def new(self, pid: str, foid: str, name: str, description: str, flags: str,
            status: str, ftype: str, priority: int) -> tuple:
        '''new is used to create new features into the database

        Args:
            pid (str): id of associated project
            foid (str): id of associated feature owner
            name (str): name of feature
            description (str): description of feature
            flags (str): flags used to identify features,
                given in string, example = 'one;two;flags;'
            status (str): status of feature, for example
                'in progress', 'waiting', 'ready', 'postponed'
            ftype (str): type of feature, for example 'new feature', 'bug fixes'
            priority (int): priority of feature, in three stages:
                low, medium and high (1 = low, 3 = high)

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database

        Returns:
            tuple: created feature's id, creation and updated on time
        '''

        values = {
            'project_id': pid,
            'feature_owner': foid,
            'name': name,
            'description': description,
            'flags': flags,
            'status': status,
            'type': ftype,
            'priority': priority
        }

        sql = '''
            INSERT INTO Features
            (project_id, feature_owner, name, description, flags, status, type, priority)
            VALUES (:project_id, :feature_owner, :name, :description, :flags, :status, :type, :priority)
            RETURNING id, created, updated_on
        '''

        try:
            feature_id, created, updated_on = db.session.execute(
                sql, values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException('While saving new feature') from error

        if not feature_id:
            raise DatabaseException('While saving new feature')

        return (feature_id, created, updated_on)

    def get_all(self) -> [tuple]:
        '''get_all is used to list of all features in the database

        If no features found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of all features
        '''

        sql = '''
            SELECT F.id, F.project_id, P.name, F.feature_owner, U.firstname, U.lastname, F.name, F.description, F.status, S.name, F.type, T.name, F.priority, F.created, F.updated_on, F.flags  
            FROM Features F
            JOIN Projects P ON F.project_id = P.id
            JOIN Users U ON F.feature_owner = U.id
            JOIN Types T ON T.id = F.type
            JOIN Statuses S ON S.id = F.status
        '''

        try:
            features = db.session.execute(sql).fetchall()
        except Exception as error:
            raise DatabaseException('While getting all features') from error

        return [(feature[0], feature[1], feature[2], feature[3], feature[4],
                 feature[5], feature[6], feature[7], feature[8], feature[9],
                 feature[10], feature[11], feature[12], feature[13],
                 feature[14], feature[15]) for feature in features]

    def get_features(self) -> [tuple]:
        '''get_features is used to get all features for
           selecting features in the frontend

        If no features found, returns empty list.

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of feature id and name
        '''

        sql = '''
            SELECT id, name
            FROM Features
        '''

        try:
            features = db.session.execute(sql).fetchall()
        except Exception as error:
            raise DatabaseException('While getting all features') from error

        return [(feature[0], feature[1]) for feature in features]

    def get_all_by_project_id(self, pid: str) -> [tuple]:
        '''get_all_by_project_id is used to get all features
           associated with given project

        If no features found, returns empty list.

        Args:
            pid (str): id of the project in which features are associated

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of found features
        '''

        sql = '''
            SELECT F.id, F.project_id, P.name, F.feature_owner, U.firstname, U.lastname, F.name, F.description, F.status, S.name, F.type, T.name, F.priority, F.created, F.updated_on, F.flags  
            FROM Features F
            JOIN Projects P ON F.project_id = P.id
            JOIN Users U ON F.feature_owner = U.id
            JOIN Types T ON T.id = F.type
            JOIN Statuses S ON S.id = F.status
            WHERE P.id=:id
        '''

        try:
            features = db.session.execute(sql, {'id': pid}).fetchall()
        except Exception as error:
            raise DatabaseException(
                'While getting features by Project ID') from error

        return [(feature[0], feature[1], feature[2], feature[3], feature[4],
                 feature[5], feature[6], feature[7], feature[8], feature[9],
                 feature[10], feature[11], feature[12], feature[13],
                 feature[14], feature[15]) for feature in features]

    def get_all_by_feature_owner(self, foid: str) -> [tuple]:
        '''get_all_by_feature_owner is used get all features
           associated with given feature owner

        If no features found, returns empty list.

        Args:
            foid (str): id of the feature owner

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database

        Returns:
            [tuple]: list of found features
        '''

        sql = '''
            SELECT F.id, F.project_id, P.name, F.feature_owner, U.firstname, U.lastname, F.name, F.description, F.status, S.name, F.type, T.name, F.priority, F.created, F.updated_on, F.flags  
            FROM Features F
            JOIN Projects P ON F.project_id = P.id
            JOIN Users U ON F.feature_owner = U.id
            JOIN Types T ON T.id = F.type
            JOIN Statuses S ON S.id = F.status
            WHERE F.feature_owner=:id
        '''

        try:
            features = db.session.execute(sql, {'id': foid}).fetchall()
        except Exception as error:
            raise DatabaseException(
                'While getting features by Feature Owner') from error

        return [(feature[0], feature[1], feature[2], feature[3], feature[4],
                 feature[5], feature[6], feature[7], feature[8], feature[9],
                 feature[10], feature[11], feature[12], feature[13],
                 feature[14], feature[15]) for feature in features]

    def get_by_id(self, fid: str) -> tuple:
        '''get_by_id is used to found feature with given id

        Args:
            fid (str): id of the feature

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if there is none features with given id

        Returns:
            tuple: found feature
        '''

        sql = '''
            SELECT F.id, F.project_id, P.name, F.feature_owner, U.firstname, U.lastname, F.name, F.description, F.status, S.name, F.type, T.name, F.priority, F.created, F.updated_on, F.flags  
            FROM Features F
            JOIN Projects P ON F.project_id = P.id
            JOIN Users U ON F.feature_owner = U.id
            JOIN Types T ON T.id = F.type
            JOIN Statuses S ON S.id = F.status
            WHERE F.id=:id
        '''

        try:
            feature = db.session.execute(sql, {'id': fid}).fetchone()
        except Exception as error:
            raise DatabaseException('While getting the feature') from error

        if not feature:
            raise NotExistingException('Feature')

        return (feature[0], feature[1], feature[2], feature[3], feature[4],
                feature[5], feature[6], feature[7], feature[8], feature[9],
                feature[10], feature[11], feature[12], feature[13], feature[14],
                feature[15])

    def get_name(self, fid: str) -> str:
        '''get_name is used to get name of feature with given id

        Args:
            fid (str): id of the feature

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
            NotExistingException: raised if feature is not
                found with given id

        Returns:
            str: found name
        '''

        sql = '''
            SELECT name
            FROM Features
            WHERE id=:id
        '''

        try:
            name = db.session.execute(sql, {'id': fid}).fetchone()
        except Exception as error:
            raise DatabaseException("While getting feature's name") from error

        if not name:
            raise NotExistingException('Feature')

        return name[0]

    def update(self, fid: str, pid: str, foid: str, name: str, description: str,
               flags: str, status: str, ftype: str, priority: int) -> tuple:
        '''update is used to update feature with given values into the database

        Args:
            fid (str): id of the feature to be updated
            pid (str): id of the associated project
            foid (str): id of the associated feature owner
            name (str): name of the feature
            description (str): description of the feature
            flags (str): flags used to identify features,
                given in string, example = 'one;two;flags;'
            status (str): status of feature, for example
                'in progress', 'waiting', 'ready', 'postponed'
            ftype (str): type of feature, for example
                'new feature', 'bug fixes'
            priority (int): priority of feature, in three stages:
                low, medium and high (1 = low, 3 = high)

        Raises:
            DatabaseException: raised if problems occurs while
                saving into the database

        Returns:
            tuple: updated feature's id, creation and updated on time
        '''

        values = {
            'project_id': pid,
            'feature_owner': foid,
            'name': name,
            'description': description,
            'flags': flags,
            'status': status,
            'type': ftype,
            'priority': priority
        }

        sql = '''
            UPDATE Features
            SET project_id=:project_id, feature_owner=:feature_owner, name=:name, description=:description, flags=:flags, status=:status, type=:type, priority=:priority
            WHERE id=:id
            RETURNING id, created, updated_on
        '''

        try:
            feature_id, created, updated_on = db.session.execute(
                sql, values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException('While saving updated feature') from error

        if str(fid) != str(feature_id):
            raise DatabaseException('While saving updated feature')

        return (feature_id, created, updated_on)

    def remove(self, fid: str) -> None:
        '''remove is used to remove feature from the database

        Args:
            fid (str): id of the feature to be removed

        Raises:
            DatabaseException: raised if problems occur
                while interacting with the database
        '''

        sql = '''
            DELETE FROM Features 
            WHERE id=:id
        '''

        try:
            db.session.execute(sql, {'id': fid})
            db.session.commit()
        except Exception as error:
            raise DatabaseException('While removing the feature') from error


feature_repository = FeatureRepository()
