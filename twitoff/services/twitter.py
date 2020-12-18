"""
Module to interact with Twitter and the backend of Twitoff
"""
from os import getenv
import tweepy
import spacy
from twitoff.models import DB, Tweet, User

# Create global Variables for twitter
TWITTER_AUTH = tweepy.OAuthHandler(getenv("TWITTER_API_KEY"),
                                   getenv("TWITTER_API_SECRET_KEY"))
TWITTER = tweepy.API(TWITTER_AUTH)

# Create the Natural Language Processing model for the tweet analysis
nlp_model = spacy.load("twitoff_nlp_model")


def vectorize_text(text):
    """Vectorize the text so that the text can be used in Linear Regression"""
    return nlp_model(text).vector


def add_or_update_user(username):
    """Adds user with username 'username' to our database"""
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, name=username))

        new_tweets = twitter_user.timeline(count=200,
                                           exclude_replies=True,
                                           include_rts=False,
                                           tweet_mode="extended")

        DB.session.add(db_user)

        existing_tweets = Tweet.query.filter_by(user_id=db_user.id).all()

        for tweet in new_tweets:
            vectorized_tweet = vectorize_text(tweet.full_text)
            db_tweet = (Tweet.query.get(tweet.id) or
                        Tweet(id=tweet.id,
                        user_id=db_user.id,
                        text=tweet.full_text,
                        embedding=vectorized_tweet))

            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print(f"Error processing {username}: {e}")
        raise e
    DB.session.commit()
