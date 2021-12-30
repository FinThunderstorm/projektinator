from flask import Flask
import utils.config as configs

app = Flask(__name__)
app.secret_key = configs.secret

if configs.mode != 'TEST':
    import routes.base    # noqa
    import routes.users    # noqa
