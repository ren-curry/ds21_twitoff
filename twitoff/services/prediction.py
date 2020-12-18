
"""Predictions of users based on tweet embeddings"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from twitoff.services.twitter import vectorize_text
from twitoff.models import User


def binary_predict_user(user0_name, user1_name, predict_tweet_text):
    """
    Determine and return which user is more likely to say a hypothetical tweet.
    Example run: predict_user("elonmusk", "jackblack",
                              "School of rock really rocks")
    Returns 0 (user0_name = elonmusk) or 1 (user1name = jackblack)
    """

    # grabbing users from our database
    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()

    # grabbing vectors from each tweet in user.tweets
    # user0_vects = np.array([tweet.embedding for tweet in user0.tweets])
    # user1_vects = np.array([tweet.embedding for tweet in user1.tweets])
    features = []
    labels = []

    for tweet in user0.tweets:
        features.append(tweet.embedding)
        labels.append(user0.name)

    for tweet in user1.tweets:
        features.append(tweet.embedding)
        labels.append(user1.name)

    # train model and instantiate
    log_reg = LogisticRegression().fit(features, labels)

    # using nlp model to generate embeddings - vectorize_tweet() - and reshapes
    predict_tweet_vect = vectorize_text(predict_tweet_text).reshape(1, -1)

    # predicts and returns 0 or 1 depending upon Logistic Regression
    # models prediction
    return log_reg.predict(predict_tweet_vect)
