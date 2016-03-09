# -*- coding: utf-8 -*
from flask import render_template, redirect, request, url_for, flash, current_app
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from .. import db
from ..models import Comment
from . import comment
from .forms import CommentForm
from datetime import datetime

@comment.route('/delete_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first_or_404()
    if comment.topic:
            tid = comment.topic.id
            db.session.delete(comment)
            return redirect(url_for('topic.show_topic', id=tid))
    else:
            tid = comment.note.id
            db.session.delete(comment)
            return redirect(url_for('note.show_note', id=tid))
    
@comment.route('/edit_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_comment(id):
    form = CommentForm()

    if form.validate_on_submit():
        comment.contents = form.body.data
        comment.lastupdate_timestamp = datetime.utcnow()
        db.session.add(comment)
        if comment.topic:
            return redirect(url_for('topic.show_topic', id=comment.topic.id))
        else:
            return redirect(url_for('note.show_note', id=comment.note.id))            
    form.body.data = comment.contents
    return render_template("comment/edit_comment.html", form=form)
    
