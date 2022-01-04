from app import app
from flask import render_template, session
from services.project_service import project_service
from services.feature_service import feature_service
from services.task_service import task_service
from services.comment_service import comment_service
from services.team_service import team_service


@app.route("/")
def index():
    try:
        user_id = session["user"]

        projects = project_service.get_all_by_project_owner(user_id)
        features = feature_service.get_all_by_feature_owner(user_id)
        tasks = task_service.get_all_by_assignee(user_id)
        comments = comment_service.get_by_assignee(user_id)
        teams = team_service.get_by_team_leader(user_id)

        return render_template("index.html",
                               projects=projects,
                               features=features,
                               tasks=tasks,
                               comments=comments,
                               teams=teams)
    except KeyError:
        return render_template("index.html")


@app.route("/health")
def health():
    return "PONG"