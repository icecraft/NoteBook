from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User, Topic, Note
from . import main
from flask.ext.login import login_required, current_user


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

