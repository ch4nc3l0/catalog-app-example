from index import db
from flask_login import UserMixin
from index import logMan


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    picurl = db.Column(db.String(2000))

    def __init__(self, id, username, picurl):
        self.id = id
        self.username = username
        self.picurl = picurl

    def __repr__(self):
        return '<id {}>'.format(self.id)


@logMan.user_loader
def load_user(id):
    return User.query.get(int(id))


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Item(db.Model):
    __tablename__ = 'item'
    category = db.relationship(Category)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    description = db.Column(db.String(1000), nullable=False)
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.TIMESTAMP)

    def __init__(self, category, category_id, description, id, name):
        self.id = category
        self.name = category_id
        self.id = description
        self.id = id
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)
