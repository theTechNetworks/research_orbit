from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    # Relationship with ResearchTopic
    topics = db.relationship('ResearchTopic', back_populates='user') 

    # Relationship with Papers
    papers = db.relationship('Papers', back_populates='user') #

    # Relationship with Notes
    notes = db.relationship('Note', back_populates='user')


class ResearchTopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    research_type = db.Column(db.String(100))
    organization = db.Column(db.String(100))
    description = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Relationship with User
    user = db.relationship('User', back_populates='topics')

    # Relationship with Papers
    papers = db.relationship('Papers', back_populates='topic', cascade="all, delete-orphan")

    #method to count paper
    def count_papers(self):
        return len(self.papers)


class Papers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10000))
    doi = db.Column(db.String(40),nullable=True)
    ISBN = db.Column(db.String,nullable=True)
    author = db.Column(db.String(1000))
    abstract = db.Column(db.String(100000), nullable=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    topic_id = db.Column(db.Integer, db.ForeignKey('research_topic.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Relationship with User
    user = db.relationship('User', back_populates='papers')

    # Relationship with ResearchTopic
    topic = db.relationship('ResearchTopic', back_populates='papers')

    # Relationship with Notes
    notes = db.relationship('Note', back_populates='paper', cascade="all, delete-orphan")


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.id'))

    # Relationship with User
    user = db.relationship('User', back_populates='notes')

    # Relationship with Papers
    paper = db.relationship('Papers', back_populates='notes')
