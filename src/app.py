from flask import Flask
import utils.config as configs

app = Flask(__name__)
app.secret_key = configs.secret

if not configs.test:
    import routes  # noqa
