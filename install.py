from dotenv import load_dotenv
import psycopg2
import os
from werkzeug.security import generate_password_hash
load_dotenv()

database_url = "sd"
print('Starting release check')

db_conn = psycopg2.connect(os.getenv("DATABASE_URL"))
db = db_conn.cursor()

#lets check if role admin exists
sql = "SELECT name FROM Roles WHERE id=%s"
result = db.execute(sql, [1])
if result == None:
    try:
        sql = "INSERT INTO Roles (name) VALUES (%s)"
        db.execute(sql, ["admin"])
        db_conn.commit()
    except:
        pass

# lets check if user admin exists
admin_username = os.getenv("ADMIN_USER")
admin_password = os.getenv("ADMIN_PASSWORD")
sql = "SELECT username FROM Users WHERE username=%s"
result = db.execute(sql, [admin_username])
if result == None:
    password_hash = generate_password_hash(admin_password)
    values = {
        "username": admin_username.lower(),
        "user_role": 1,
        "password_hash": password_hash,
        "name": "Admin User",
        "email": "admin@mail.mail"
    }
    try:
        sql = "INSERT INTO Users (username, user_role, password_hash, name, email) VALUES (%s, %s, %s, %s, %s)"
        db.execute(sql, [
            admin_username.lower(), 1, password_hash, "Admin User",
            "admin@mail.mail"
        ])
        db_conn.commit()
    except Exception as error:
        print('>', error)
print('ready')