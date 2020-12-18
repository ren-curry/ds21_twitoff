from flask import Blueprint, render_template, request, flash, redirect
from twitoff.models import DB, User
from twitoff.services.twitter import add_or_update_user

data_routes = Blueprint("data_routes", __name__)


@data_routes.route("/user", methods=["POST"])
@data_routes.route("/user/<name>", methods=["GET"])
def user(name=None, message=""):
    name = name or request.values["user_name"]
    try:
        if request.method == "POST":
            add_or_update_user(name)
            message = "User {} sucessfully added!".format(name)

        tweets = User.query.filter(User.name == name).one().tweets

    except Exception as e:
        message = "Error handling {}: {}".format(name, e)
        tweets = []

    return render_template("user.html",
                           title=name,
                           tweets=tweets,
                           message=message)
