from db import db
from datetime import datetime
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash


def add_project(name, description, flags):
    sql = "INSERT INTO Projects (name, description, flags, added_on) VALUES (:name, :description, :flags, :added_on)"
    values = {
        "name": name,
        "description": description,
        "flags": flags,
        "added_on": datetime.now()
    }
    try:
        db.session.execute(sql, values)
        db.session.commit()
        return True
    except Exception as error:
        print('>', error)
        return False


def get_project(id=None):
    if id == None:
        sql = "SELECT * FROM Projects"
        result = db.session.execute(sql)
        return result.fetchall()
    else:
        sql = "SELECT * FROM Projects WHERE id=:id"
        result = db.session.execute(sql, {"id": id})
        return result.fetchone()


def remove_project(id):
    sql = "DELETE FROM Projects WHERE id=:id"
    try:
        db.session.execute(sql, {"id": id})
        db.session.commit()
        return True
    except:
        return False


def update_project(id, name, description, flags, added_on):
    sql = "UPDATE Projects SET name=:name, description=:description, flags=:flags, added_on=:added_on WHERE id=:id"
    values = {
        "name": name,
        "description": description,
        "flags": flags,
        "added_on": added_on,
        "id": id
    }
    try:
        db.session.execute(sql, values)
        db.session.commit()
        return True
    except:
        return False


def add_role(name):
    try:
        sql = "INSERT INTO Roles (name) VALUES (:name)"
        db.session.execute(sql, {"name": name})
        db.session.commit()
    except:
        pass


def add_team(name):
    try:
        sql = "INSERT INTO Teams (name) VALUES (:name)"
        db.session.execute(sql, {"name": name})
        db.session.commit()
    except:
        pass


def login(username, password):
    sql = "SELECT id, password_hash FROM Users WHERE username=:username"
    result = db.session.execute(sql, {"username": username.lower()})
    user = result.fetchone()
    if user == None:
        return None
    id, password_hash = user
    if check_password_hash(password_hash, password):
        return {"id": id, "username": username}
    return None


def get_all_users():
    sql = "SELECT id,name, username, email, user_role FROM Users"
    result = db.session.execute(sql)
    return result.fetchall()


def find_user(id):
    sql = "SELECT id, name, username, email, user_role FROM Users WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()


def add_user(username, password, name, email, user_role):
    password_hash = generate_password_hash(password)
    user_role = int(user_role)
    values = {
        "username": username.lower(),
        "user_role": user_role,
        "password_hash": password_hash,
        "name": name,
        "email": email
    }
    try:
        # INSERT INTO Users (username, user_role, password_hash, name, email) VALUES ("tuki", 1, "pbkdf2:sha256:150000$5a5GwUss$8137fb4128bc8dddef9f51e97d22853ad82ccdc4f07960caafd1b137c2e08ac0", "Tuki", "tuki@paaryna.fi");
        sql = "INSERT INTO Users (username, user_role, password_hash, name, email) VALUES (:username, :user_role, :password_hash, :name, :email)"
        db.session.execute(sql, values)
        db.session.commit()
        return True
    except Exception as error:
        print('>', error)
        return False


def remove_user(id):
    sql = "DELETE FROM Users WHERE id=:id"
    try:
        db.session.execute(sql, {"id": id})
        db.session.commit()
        return True
    except:
        return False


def update_user(id, username, user_role, password, name, email):
    user_role = int(user_role)
    if password != "":
        password_hash = generate_password_hash(password)
        sql = "UPDATE Users SET username=:username, user_role=:user_role, password_hash=:password_hash, name=:name, email=:email WHERE id=:id"
        values = {
            "username": username.lower(),
            "user_role": user_role,
            "password_hash": password_hash,
            "name": name,
            "email": email,
            "id": id
        }
        try:
            db.session.execute(sql, values)
            db.session.commit()
            return True
        except:
            return False
    else:
        sql = "UPDATE Users SET username=:username, user_role=:user_role, name=:name, email=:email WHERE id=:id"
        values = {
            "username": username.lower(),
            "user_role": user_role,
            "name": name,
            "email": email,
            "id": id
        }
        try:
            db.session.execute(sql, values)
            db.session.commit()
            return True
        except:
            return False
