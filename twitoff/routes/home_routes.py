from flask import Blueprint, render_template, redirect
from twitoff.models import DB, User
from twitoff.services.twitter import add_or_update_user

home_routes = Blueprint("home_routes", __name__)


@home_routes.route('/')
def root():
    try:
        users = User.query.all()
    except Exception as e:
        DB.drop_all()
        DB.create_all()
        users = User.query.all()
    return render_template('base.html', title='Home', users=users)


@home_routes.route('/update')
def update():
    users = User.query.all()
    for user in users:
        add_or_update_user(user.name)
    return redirect("/")


@home_routes.route('/reset')
def reset():
    DB.drop_all()
    DB.create_all()
    return redirect("/")
