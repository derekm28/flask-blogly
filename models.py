"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


class User(db.Model):
    """User"""

    __tablename__ =  'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.Text(50), nullable = False, unique = False)
    last_name = db.Column(db.Text(50), nullable = False, unique = False)
    image_url = db.Column(db.Text, nullable = False, default = DEFAULT_IMAGE_URL)
    posts = db.relationship('Post', backref = 'user')

    posts = db.relationship('Post', backref = 'user', cascade = 'all, delete-orphan')

    @property
    def full_name(self):
        """return full name of user"""
        return f'{self.first_name} {self.last_name}'

class Post(db.Model):
    """Post"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.Text(50), nullable = False, unique = False)
    content = db.Column(db.Text(140), nullable = False, unique = False)
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    #user = db.relationship('User')

    @property
    def friendly_date(self):
        """return formatted date"""

        return self.created_at.strftime('%a %b %-d %Y, %-I:%M %p')



class PostTag(db.Model):
    """Post Tag"""

    __tablename__ = 'posts_tags'

    #id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True, nullable = False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True, nullable = False)


class Tag(db.Model):
    """Tag"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text(50), nullable = False, unique = True)

    posts = db.relationship(
        'Post',
        secondary = 'posts_tags',
        # cascade = 'all, delete',
        backref = 'tags'
    )


def connect_db(app):
    """connect this database to provided Flask app, You should call this in your Flask app"""

    db.app = app
    db.init_app(app)
