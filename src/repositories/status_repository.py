from utils.database import db
from utils.exceptions import DatabaseException, NotExistingException


class StatusRepository:

    def new(self, name: str):
        sql = """
        INSERT INTO Statuses
        (name)
        VALUES (:name)
        RETURNING id
        """

        values = {"name": name}

        try:
            sid = db.session.execute(sql, values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException(
                'While saving new status into database') from error

        if not sid:
            raise DatabaseException(
                'While saving new status into database') from error

        return (sid, name)

    def get_all(self):
        sql = "SELECT id, name FROM Statuses"
        try:
            statuses = db.session.execute(sql).fetchall()
        except Exception as error:
            raise DatabaseException('while getting all statuses') from error

        return [(status[0], status[1]) for status in statuses]

    def get_by_id(self, sid: str):
        sql = "SELECT id, name FROM Statuses WHERE id=:id"
        try:
            status = db.session.execute(sql, {"id": sid}).fetchone()
        except Exception as error:
            raise DatabaseException('while getting status') from error

        return (status[0], status[1])

    def get_name(self, sid: str):
        sql = "SELECT name FROM Statuses WHERE id=:id"
        try:
            status = db.session.execute(sql, {"id": sid}).fetchone()
        except Exception as error:
            raise DatabaseException('while getting status') from error

        return status

    def update(self, sid: str, name: str):
        values = {"id": sid, "name": name}
        sql = """
        UPDATE Projects 
        SET name=:name
        WHERE id=:id 
        RETURNING id
        """
        try:
            status_id = db.session.execute(sql, values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException(
                'While saving updated status into database') from error
        if str(sid) != str(status_id):
            raise DatabaseException('While saving updated status into database')

        return (status_id, name)

    def remove(self, sid: str):
        sql = "DELETE FROM Statuses WHERE id=:id"
        try:
            db.session.execute(sql, {"id": sid})
            db.session.commit()
        except Exception as error:
            raise DatabaseException('status remove') from error


status_repository = StatusRepository()