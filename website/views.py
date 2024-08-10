from flask import render_template,request,flash ,Blueprint, jsonify,url_for,redirect
from flask_login import login_required,current_user
from . import db
import json
from .models import ResearchTopic

#define file as blueprint
views = Blueprint("views",__name__)


#defining routes
@views.route('/')
def home():
    return render_template("home.html")


@views.route('/about')
def about():
    return render_template("about.html")


@views.route('/landing',methods=['POST','GET'])
@login_required
def landing():
    topics = ResearchTopic.query.filter_by(user_id=current_user.id).all()
    return render_template('landing.html',topics=topics)


@views.route('/topics')
@login_required
def view_topics():
    topics = ResearchTopic.query.filter_by(user_id=current_user.id).all()
    return render_template('topics.html', topics=topics)

@views.route('/topics/<int:topic_id>', methods=['GET'])
@login_required
def view_topic(topic_id):
    topic = ResearchTopic.query.get_or_404(topic_id)
    paper_count = topic.count_papers()
    return render_template('topic_detail.html', topic=topic,paper_count=paper_count)

@views.route('/delete_topic/<int:topic_id>', methods=['POST'])
@login_required
def delete_topic(topic_id):
    topic = ResearchTopic.query.get_or_404(topic_id)
    if topic.user_id != current_user.id:
        flash('You do not have permission to delete this topic.', category='error')
        return redirect(url_for('views.view_topics'))
    
    db.session.delete(topic)
    db.session.commit()
    flash('Research topic deleted successfully.', category='success')
    return redirect(url_for('views.view_topics'))


@views.route('/papers',methods=['GET','POST'])
@login_required
def view_papers():
    return render_template('papers.html',User= current_user)