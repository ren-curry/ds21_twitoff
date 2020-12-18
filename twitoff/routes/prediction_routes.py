from flask import Blueprint, render_template, request, redirect
from twitoff.models import DB, User
from twitoff.services.prediction import binary_predict_user
from twitoff.services.twitter import add_or_update_user

prediction_routes = Blueprint("prediction_routes", __name__)


@prediction_routes.route("/compare", methods=["POST"])
def compare():
    user0, user1 = sorted(
        [request.values["user1"], request.values["user2"]])

    # conditinoal that prevents same user comparison
    if user0 == user1:
        message = "Cannot compare users to themselves!"

    else:
        predict_tweet_text = request.values["tweet_text"]
        # prediction return zero or one depending upon user
        prediction = binary_predict_user(user0, user1, predict_tweet_text)
        message = "The tweet is more likely to be said by {} than {}".format(
            user1 if prediction == user1 else user0,
            user0 if prediction == user1 else user1
            )

    # returns rendered template with dynamic message
    return render_template('prediction.html',
                           title="Prediction:",
                           message=message)
