from app import db
from flask_security import UserMixin

roles_user = db.Table('roles_user',
                      db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                      db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), unique=True)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_user, backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

