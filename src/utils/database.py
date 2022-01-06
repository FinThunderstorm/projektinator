from app import app
from flask_sqlalchemy import SQLAlchemy
import utils.config as configs

db_uri = configs.database_url

if db_uri.startswith('postgres://'):
    db_uri = db_uri.replace('postgres://', 'postgresql://', 1)

print(db_uri)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
# let's get rid of annoying warning in the logs.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
