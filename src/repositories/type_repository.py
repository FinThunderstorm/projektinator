from utils.database import db
from utils.exceptions import DatabaseException, NotExistingException


class TypeRepository:

    def new(self, name: str):
        sql = """
        INSERT INTO Types
        (name)
        VALUES (:name)
        RETURNING id
        """

        values = {"name": name}

        try:
            tyid = db.session.execute(sql, values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException(
                'While saving new type into database') from error

        if not tyid:
            raise DatabaseException(
                'While saving new type into database') from error

        return (tyid, name)

    def get_all(self):
        sql = "SELECT id, name FROM Types"
        try:
            types = db.session.execute(sql).fetchall()
        except Exception as error:
            raise DatabaseException('while getting all types') from error

        return [(type[0], type[1]) for type in types]

    def get_by_id(self, tyid: str):
        sql = "SELECT id, name FROM Types WHERE id=:id"
        try:
            type = db.session.execute(sql, {"id": tyid}).fetchone()
        except Exception as error:
            raise DatabaseException('while getting types') from error

        return (type[0], type[1])

    def get_name(self, tyid: str):
        sql = "SELECT name FROM Types WHERE id=:id"
        try:
            type = db.session.execute(sql, {"id": tyid}).fetchone()
        except Exception as error:
            raise DatabaseException('while getting types') from error

        return type

    def update(self, tyid: str, name: str):
        values = {"id": tyid, "name": name}
        sql = """
        UPDATE Types 
        SET name=:name
        WHERE id=:id 
        RETURNING id
        """
        try:
            type_id = db.session.execute(sql, values).fetchone()
            db.session.commit()
        except Exception as error:
            raise DatabaseException(
                'While saving updated type into database') from error
        if str(tyid) != str(type_id):
            raise DatabaseException('While saving updated type into database')

        return (type_id, name)

    def remove(self, tyid: str):
        sql = "DELETE FROM Types WHERE id=:id"
        try:
            db.session.execute(sql, {"id": tyid})
            db.session.commit()
        except Exception as error:
            raise DatabaseException('type remove') from error


type_repository = TypeRepository()
