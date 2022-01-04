from utils.database import db
from utils.exceptions import DatabaseException, NotExistingException


class RoleRepository:

    def get_all(self):
        sql = "SELECT id, name, description FROM Roles"
        try:
            roles = db.session.execute(sql).fetchall()
        except Exception as error:
            raise DatabaseException('while getting all roles') from error

        return [(role[0], role[1], role[2]) for role in roles]

    def get_by_id(self, rid: str):
        sql = "SELECT id, name, description FROM Roles"
        try:
            role = db.session.execute(sql, {"id": rid}).fetchone()
        except Exception as error:
            raise DatabaseException('while getting roles') from error

        return (role[0], role[1], role[2])

    def get_name(self, rid: str):
        sql = "SELECT name FROM Roles WHERE id=:id"
        try:
            name = db.session.execute(sql, {"id": rid}).fetchone()[0]
        except Exception as error:
            raise DatabaseException('while getting role') from error

        return name


role_repository = RoleRepository()
