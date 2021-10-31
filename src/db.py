from app import app
from flask_sqlalchemy import SQLAlchemy
import utils.config as configs

print(configs.database_url)


app.config['SQLALCHEMY_DATABASE_URI'] = configs.database_url
# let's get rid of annoying warning in the logs.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
