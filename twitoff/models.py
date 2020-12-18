"""
SQLAlchemy models and utility functions for Twitoff
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate()

# Instantiate our SQLAlchemy class "Database"
DB = SQLAlchemy()
MIGRATE = Migrate()


# Database Table creations with SQLAlchemy
class User(DB.Model):
    """Twitter users corresponding to Tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return f"<User: {self.name}>"


class Tweet(DB.Model):
    """Tweet Text and Data"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300), nullable=False)
    embedding = DB.Column(DB.PickleType, nullable=False)
    # Foreign Key to User Table. **Note that the reference is lowercase
    user_id = DB.Column(DB.BigInteger,
                        DB.ForeignKey('user.id'),
                        nullable=False)
    # Builds a relationship for User-Tweets, pulls all tweets w/user.tweets
    user = DB.relationship('User', backref=DB.backref('tweets'), lazy=True)

    def __repr__(self):
        return f"<Tweet: {self.text}>"


def insert_example_records():
    """Generate example users"""
    users_to_add = []
    tweets_to_add = []

    # TODO: Add Error Handling, for now drop and recreate.
    DB.drop_all()
    DB.create_all()

    # User Creation
    users_to_add.append(User(id=1, name="Nix"))
    users_to_add.append(User(id=2, name="Seeker"))

    # Tweet Creation
    tweets_to_add.append(Tweet(id=1,
                               text="A rogue, a changeling rogue.",
                               user_id=1,
                               user=users_to_add[0]))
    tweets_to_add.append(Tweet(id=2,
                               text="Little tricks of the arcane kind.",
                               user_id=1,
                               user=users_to_add[0]))
    tweets_to_add.append(Tweet(id=3,
                               text="Sneak, Sneak, Sneak, MAGE HAND.",
                               user_id=1,
                               user=users_to_add[0]))
    tweets_to_add.append(Tweet(id=4,
                               text="A sorcerer, a tiefling sorcerer.",
                               user_id=2,
                               user=users_to_add[1]))
    tweets_to_add.append(Tweet(id=5,
                               text="Blood of dragons and an outfit to match.",
                               user_id=2,
                               user=users_to_add[1]))
    tweets_to_add.append(Tweet(id=6,
                               text="FIREBALL.",
                               user_id=2,
                               user=users_to_add[1]))

    for user in users_to_add:
        DB.session.add(user)

    for tweet in tweets_to_add:
        DB.session.add(tweet)
    DB.session.commit()
