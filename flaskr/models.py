from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flaskr import db
from flaskr.utils import slugify


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(180), unique=True)
    password = db.Column(db.String(255))
    about = db.Column(db.Text, nullable=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    def setpassword(self, password):
        self.password = generate_password_hash(password)

    def checkpassword(self, password):
        return check_password_hash(self.password, password)


tags = db.Table('posts_tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
                db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
                )


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    title = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    text = db.Column(db.Text)
    html = db.Column(db.Text)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('posts', lazy=True))
    isPrivate = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)  # auto_now_add=True
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = slugify(self.title)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
