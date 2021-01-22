from db import db
import os
import queries

#lets check if role admin exists
sql = "SELECT name FROM Roles WHERE id=id"
result = db.session.execute(sql, {"id": 1})
if result.fetchone() == None:
    try:
        sql = "INSERT INTO Roles (name) VALUES (:name)"
        db.session.execute(sql, {"name": "admin"})
        db.session.commit()
    except:
        pass

# lets check if user admin exists
admin_username = os.getenv("ADMIN_USER")
admin_password = os.getenv("ADMIN_PASSWORD")
sql = "SELECT username FROM Users WHERE username=:username"
result = db.session.execute(sql, {"username": admin_username})
if result.fetchone() == None:
    queries.add_user(admin_username, admin_password, "Admin User",
                     "admin@mail.mail", 1)
