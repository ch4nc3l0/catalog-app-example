from index import db
from flask_login import UserMixin
from index import logMan


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    picurl = db.Column(db.String(2000))

    def __init__(self, username, id, picurl):
        self.username = username
        self.id = id
        self.picurl = picurl

    def __repr__(self):
        return '<id {}>'.format(self.id)


@logMan.user_loader
def load_user(id):
    return User.query.get(int(id))
