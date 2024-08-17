from flask import render_template,request,flash ,Blueprint, jsonify,url_for,redirect
from flask_login import login_required,current_user
from . import db
import json
from .models import ResearchTopic,Papers,Note

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

# viewing added papers
@views.route('/papers/<int:topic_id>',methods=['GET','POST'])
@login_required
def view_papers(topic_id):
    papers = Papers.query.filter_by(topic_id=topic_id).all()
    return render_template('papers.html',papers= papers)


# deleting added papers
@views.route('/delete_paper/<int:paper_id>', methods=['POST'])
@login_required
def delete_paper(paper_id):
    paper = Papers.query.get_or_404(paper_id)
    topic_id = paper.topic_id
    if paper.user_id != current_user.id:
        flash('You do not have permission to delete this topic.', category='error')
        return redirect(url_for('views.view_papers',topic_id=topic_id))
    
    db.session.delete(paper)
    db.session.commit()
    flash('Research topic deleted successfully.', category='success')
    return redirect(url_for('views.view_papers',topic_id=topic_id))


#view paper
@views.route('/view_paper/<int:paper_id>', methods=['GET'])
@login_required
def view_paper(paper_id):
    paper = Papers.query.get_or_404(paper_id)
    note= Note.query.filter_by(paper_id=paper_id).first()
    topic_id = paper.topic_id
    return render_template('paper_detail.html', paper=paper,topic_id=topic_id,note=note)

