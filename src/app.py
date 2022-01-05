from flask import Flask
import utils.config as configs

app = Flask(__name__)
app.secret_key = configs.secret

if configs.mode != 'TEST':
    import routes.base    # pylint: disable=unused-import
    import routes.users    # pylint: disable=unused-import
    import routes.teams    # pylint: disable=unused-import
    import routes.tasks    # pylint: disable=unused-import
    import routes.projects    # pylint: disable=unused-import
    import routes.features    # pylint: disable=unused-import
    import routes.comments    # pylint: disable=unused-import
