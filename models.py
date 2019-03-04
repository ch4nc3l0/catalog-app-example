#!/usr/bin/env python3.7.1
from index import db, ma
from flask_login import UserMixin
from index import logMan
import datetime


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
    id = db.Column(db.Integer, primary_key=True, nullable=False,
                   autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    user = db.relationship(User)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name):
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
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user = db.relationship(User)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, category_id, description, name):
        self.category_id = category_id
        self.description = description
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class CategorySchema(ma.ModelSchema):
    class Meta:
        model = Category


class ItemSchema(ma.ModelSchema):
    class Meta:
        model = Item
